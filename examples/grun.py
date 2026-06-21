#!/usr/bin/env python3
"""
argparse GUI-Runner
====================
Lädt ein beliebiges Python-Skript, das `argparse` verwendet, extrahiert
dessen ArgumentParser (ohne das Skript "richtig" laufen zu lassen) und
baut daraus automatisch ein Eingabeformular. Beim Klick auf "Ausführen"
wird das Original-Skript als Subprozess mit den eingegebenen Parametern
gestartet; die Ausgabe erscheint live im Log-Fenster.

Funktioniert mit Skripten, die irgendwo (egal ob auf Modulebene oder
in einer per `if __name__ == "__main__":` geschützten Funktion)
`argparse.ArgumentParser(...)` + `.parse_args()` / `.parse_known_args()`
aufrufen.

Start:
    pip install PyQt5
    python grun.py


            Code generated with Claude AI, June 2026
"""

import sys
import os
import runpy
import argparse
import shlex
from typing import Optional, List

import re

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QLabel,
    QPlainTextEdit,
    QTextEdit,
    QGroupBox,
    QSplitter,
    QMessageBox,
    QFileDialog,
    QScrollArea,
)
from PyQt5.QtCore import Qt, QProcess, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QPalette


# --------------------------------------------------------------------------
# 0) Minimaler ANSI-Interpreter (SGR-Farben/Stile + \r + \b + einfaches
#    Line-Erase \x1b[K), reicht für die meisten CLI-Tools (tqdm, colorama,
#    click, rich "basic" Output, ...).
# --------------------------------------------------------------------------

_ANSI_RE = re.compile(r"\x1b\[([0-9;]*)([A-Za-z])")

# Standard 16-Farben-Palette (etwas an gängige dunkle Terminalthemes angelehnt)
_ANSI_COLORS = {
    30: "#000000",
    31: "#cc0000",
    32: "#4e9a06",
    33: "#c4a000",
    34: "#3465a4",
    35: "#75507b",
    36: "#06989a",
    37: "#d3d7cf",
    90: "#555753",
    91: "#ef2929",
    92: "#8ae234",
    93: "#fce94f",
    94: "#729fcf",
    95: "#ad7fa8",
    96: "#34e2e2",
    97: "#eeeeec",
}
_ANSI_BG_COLORS = {k + 10: v for k, v in _ANSI_COLORS.items()}


class AnsiTextParser:
    """
    Wandelt einen Strom von Text mit ANSI-Escape-Sequenzen in eine Folge
    von Steueranweisungen um, die per insertText() in ein QTextEdit
    eingefügt werden können. Hält den aktuellen SGR-Zustand zwischen
    Aufrufen (für den Fall, dass eine Sequenz über zwei readyRead-Häppchen
    verteilt ankommt).
    """

    def __init__(self, base_color="#d3d7cf", base_bg="#1e1e1e"):
        self.base_color = base_color
        self.base_bg = base_bg
        self._pending = ""  # unvollständige Escape-Sequenz vom letzten Aufruf
        self.reset_state()

    def reset_state(self):
        self.fmt = QTextCharFormat()
        self.fmt.setForeground(QColor(self.base_color))
        self.bold = False

    def _apply_sgr(self, codes):
        if not codes:
            codes = [0]
        i = 0
        while i < len(codes):
            c = codes[i]
            if c == 0:
                self.reset_state()
            elif c == 1:
                self.bold = True
                f = self.fmt.font()
                f.setBold(True)
                self.fmt.setFont(f)
            elif c == 22:
                self.bold = False
                f = self.fmt.font()
                f.setBold(False)
                self.fmt.setFont(f)
            elif c == 4:
                self.fmt.setFontUnderline(True)
            elif c == 24:
                self.fmt.setFontUnderline(False)
            elif c == 39:
                self.fmt.setForeground(QColor(self.base_color))
            elif c == 49:
                self.fmt.clearBackground()
            elif c in _ANSI_COLORS:
                self.fmt.setForeground(QColor(_ANSI_COLORS[c]))
            elif c in _ANSI_BG_COLORS:
                self.fmt.setBackground(QColor(_ANSI_BG_COLORS[c]))
            elif c == 38 and i + 2 < len(codes) and codes[i + 1] == 5:
                # 256-Farben, vereinfachend: nur grobe Zuordnung
                idx = codes[i + 2]
                self.fmt.setForeground(QColor(_ANSI_COLORS.get(30 + (idx % 8), self.base_color)))
                i += 2
            elif c == 38 and i + 4 < len(codes) and codes[i + 1] == 2:
                r, g, b = codes[i + 2], codes[i + 3], codes[i + 4]
                self.fmt.setForeground(QColor(r, g, b))
                i += 4
            i += 1

    def feed(self, chunk: str):
        """
        Liefert eine Liste von Steueranweisungen:
          ("text", str, QTextCharFormat)
          ("cr",)            -> Cursor an Zeilenanfang (carriage return)
          ("erase_line",)    -> aktuelle Zeile löschen (\\x1b[2K / [K)
          ("backspace",)
        """
        ops = []
        data = self._pending + chunk
        self._pending = ""
        pos = 0
        for m in _ANSI_RE.finditer(data):
            if m.start() > pos:
                ops.extend(self._split_controls(data[pos : m.start()]))
            params, final = m.group(1), m.group(2)
            codes = [int(p) for p in params.split(";") if p != ""] if params else []
            if final == "m":
                self._apply_sgr(codes)
            elif final == "K":
                ops.append(("erase_line",))
            elif final in ("H", "f", "A", "B", "C", "D", "J"):
                pass  # Cursor-Bewegung/Screen-Clear: ignorieren (kein Full-TUI-Support)
            pos = m.end()

        tail = data[pos:]
        # mögliche unvollständige Escape-Sequenz am Ende zurückhalten
        esc_idx = tail.rfind("\x1b")
        if esc_idx != -1 and not _ANSI_RE.search(tail[esc_idx:]):
            self._pending = tail[esc_idx:]
            tail = tail[:esc_idx]
        ops.extend(self._split_controls(tail))
        return ops

    def _split_controls(self, text):
        ops = []
        buf = ""
        for ch in text:
            if ch == "\r":
                if buf:
                    ops.append(("text", buf, QTextCharFormat(self.fmt)))
                    buf = ""
                ops.append(("cr",))
            elif ch == "\b":
                if buf:
                    ops.append(("text", buf, QTextCharFormat(self.fmt)))
                    buf = ""
                ops.append(("backspace",))
            else:
                buf += ch
        if buf:
            ops.append(("text", buf, QTextCharFormat(self.fmt)))
        return ops


class TerminalPlainTextEdit(QTextEdit):
    """
    ANSI-kompatibles Mini-Terminal auf Basis von QTextEdit:
    - Programmausgabe wird angehängt und dabei interpretiert (Farben/Stile
      via SGR-Escapecodes, \\r für Carriage-Return/Progressbars, \\x1b[K
      zum Löschen der aktuellen Zeile, \\b als Backspace)
    - der Nutzer kann dahinter tippen; Enter sendet die Zeile als stdin
      an den laufenden Prozess (Signal line_entered)
    - Bearbeitung ist auf den Bereich NACH der letzten Ausgabe beschränkt
    """

    line_entered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._input_start = 0
        self.input_enabled = False
        self._ansi = AnsiTextParser()

        # klassisches dunkles Terminal-Theme
        self.setReadOnly(False)
        self.setUndoRedoEnabled(False)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        pal = self.palette()
        pal.setColor(QPalette.Base, QColor("#1e1e1e"))
        pal.setColor(QPalette.Text, QColor("#d3d7cf"))
        self.setPalette(pal)

    def append_output(self, text: str):
        """Programmausgabe (inkl. ANSI-Escapecodes) anhängen und interpretieren."""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

        for op in self._ansi.feed(text):
            if op[0] == "text":
                _, chunk, fmt = op
                self.textCursor().insertText(chunk, fmt)
            elif op[0] == "cr":
                # Cursor an den Anfang der aktuellen Zeile setzen (nachfolgender
                # Text überschreibt damit die Zeile, wie bei Progressbars üblich)
                c = self.textCursor()
                c.movePosition(QTextCursor.StartOfLine)
                self.setTextCursor(c)
            elif op[0] == "erase_line":
                c = self.textCursor()
                c.movePosition(QTextCursor.StartOfLine)
                c.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
                c.removeSelectedText()
                self.setTextCursor(c)
            elif op[0] == "backspace":
                c = self.textCursor()
                c.deletePreviousChar()
                self.setTextCursor(c)

        cur = self.textCursor()
        cur.movePosition(QTextCursor.End)
        self.setTextCursor(cur)
        self._input_start = self.textCursor().position()
        self.ensureCursorVisible()

    def clear(self):
        super().clear()
        self._ansi.reset_state()
        self._input_start = 0

    def set_input_enabled(self, enabled: bool):
        self.input_enabled = enabled
        if not enabled:
            self._input_start = self.textCursor().position()

    def keyPressEvent(self, event):
        if not self.input_enabled:
            return  # solange kein Prozess läuft: keine Tastatureingabe

        cursor = self.textCursor()
        if cursor.position() < self._input_start:
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)

        if event.key() == Qt.Key_Backspace:
            if self.textCursor().position() <= self._input_start:
                return
            super().keyPressEvent(event)
            return

        if event.key() == Qt.Key_Left:
            if self.textCursor().position() <= self._input_start:
                return
            super().keyPressEvent(event)
            return

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            line = self.toPlainText()[self._input_start :]
            super().keyPressEvent(event)  # sichtbaren Zeilenumbruch einfügen
            self._input_start = self.textCursor().position()
            self.line_entered.emit(line)
            return

        super().keyPressEvent(event)


# --------------------------------------------------------------------------
# 1) Parser-Extraktion: Skript so weit ausführen, bis parse_args() aufgerufen
#    wird, dann abbrechen und den Parser einsammeln.
# --------------------------------------------------------------------------


class _ParserCaptured(Exception):
    """Wird geworfen, sobald parse_args()/parse_known_args() abgefangen wurde."""

    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser


def extract_parser(script_path: str) -> argparse.ArgumentParser:
    """
    Führt das Skript in einem isolierten Prozess-Namespace aus und fängt
    den ersten Aufruf von ArgumentParser.parse_args()/parse_known_args() ab,
    um den fertig konfigurierten Parser zu erhalten - OHNE dass das
    eigentliche Programm (z.B. Dateiverarbeitung) tatsächlich losläuft.
    """
    orig_parse_args = argparse.ArgumentParser.parse_args
    orig_parse_known_args = argparse.ArgumentParser.parse_known_args

    def fake_parse_args(self, *a, **kw):
        raise _ParserCaptured(self)

    def fake_parse_known_args(self, *a, **kw):
        raise _ParserCaptured(self)

    argparse.ArgumentParser.parse_args = fake_parse_args
    argparse.ArgumentParser.parse_known_args = fake_parse_known_args

    old_argv = sys.argv
    try:
        sys.argv = [script_path]
        try:
            runpy.run_path(script_path, run_name="__main__")
        except _ParserCaptured as captured:
            return captured.parser
        except SystemExit:
            raise RuntimeError(
                "Das Skript hat sich beendet, bevor argparse.parse_args() "
                "aufgerufen wurde (z.B. wegen eines Fehlers oder fehlender "
                "Bedingung). Parser konnte nicht extrahiert werden."
            )
        raise RuntimeError(
            "Im Skript wurde kein ArgumentParser.parse_args()-Aufruf "
            "gefunden (evtl. wird er nicht unter "
            "`if __name__ == \"__main__\":` aufgerufen)."
        )
    finally:
        sys.argv = old_argv
        argparse.ArgumentParser.parse_args = orig_parse_args
        argparse.ArgumentParser.parse_known_args = orig_parse_known_args


# --------------------------------------------------------------------------
# 2) Dynamisches Formular aus den Actions des Parsers bauen
# --------------------------------------------------------------------------


class FieldWidget:
    """Hält Widget + Action zusammen und weiß, wie man daraus CLI-Tokens baut."""

    def __init__(self, action: argparse.Action, widget, kind: str):
        self.action = action
        self.widget = widget
        self.kind = kind  # 'bool' | 'choice' | 'text' | 'positional'

    def primary_flag(self) -> Optional[str]:
        if not self.action.option_strings:
            return None
        # bevorzugt die lange Form
        long_opts = [o for o in self.action.option_strings if o.startswith("--")]
        return long_opts[0] if long_opts else self.action.option_strings[0]

    def to_argv(self) -> List[str]:
        is_positional = not self.action.option_strings

        if self.kind == "bool":
            checked = self.widget.isChecked()
            if not checked:
                return []
            return [self.primary_flag()]

        text = self.widget.currentText() if self.kind == "choice" else self.widget.text()
        text = text.strip()

        if text == "":
            return []

        if self.action.nargs in ("*", "+"):
            tokens = shlex.split(text)
        else:
            tokens = [text]

        if is_positional:
            return tokens
        return [self.primary_flag(), *tokens]

    def is_required_but_empty(self) -> bool:
        required = bool(getattr(self.action, "required", False)) or not self.action.option_strings
        if self.kind == "bool":
            return False
        if not required:
            return False
        text = self.widget.currentText() if self.kind == "choice" else self.widget.text()
        return text.strip() == "" and self.action.default in (None, argparse.SUPPRESS)


class ArgFormBuilder:
    """Baut für einen ArgumentParser ein QFormLayout mit passenden Eingabefeldern."""

    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser
        self.fields: List[FieldWidget] = []

    def build(self) -> QWidget:
        container = QWidget()
        form = QFormLayout(container)
        form.setSpacing(8)

        for action in self.parser._actions:
            if isinstance(action, argparse._HelpAction):
                continue
            field = self._build_field(action)
            if field is None:
                continue
            self.fields.append(field)
            label_text = self._label_for(action)
            form.addRow(label_text, field.widget)
            if action.help:
                help_lbl = QLabel(f"<i>{action.help}</i>")
                help_lbl.setStyleSheet("color: #666; font-size: 11px;")
                help_lbl.setWordWrap(True)
                form.addRow("", help_lbl)

        return container

    def _label_for(self, action: argparse.Action) -> str:
        if action.option_strings:
            name = "/".join(action.option_strings)
        else:
            name = action.dest
        required = bool(getattr(action, "required", False)) or not action.option_strings
        suffix = " *" if required else ""
        return f"{name}{suffix}:"

    def _build_field(self, action: argparse.Action) -> Optional[FieldWidget]:
        # store_true / store_false -> Checkbox
        if isinstance(action, (argparse._StoreTrueAction, argparse._StoreFalseAction)):
            cb = QCheckBox()
            cb.setChecked(bool(action.default) if isinstance(action.default, bool) else False)
            return FieldWidget(action, cb, "bool")

        # choices -> Combobox
        if action.choices:
            combo = QComboBox()
            combo.setEditable(False)
            items = [str(c) for c in action.choices]
            combo.addItems(items)
            if action.default is not None and str(action.default) in items:
                combo.setCurrentText(str(action.default))
            return FieldWidget(action, combo, "choice")

        # alles andere (str/int/float/Liste/positional) -> Textfeld
        edit = QLineEdit()
        if action.default not in (None, argparse.SUPPRESS):
            if isinstance(action.default, (list, tuple)):
                edit.setText(" ".join(str(x) for x in action.default))
            else:
                edit.setText(str(action.default))
        placeholder_bits = []
        if action.type is not None and hasattr(action.type, "__name__"):
            placeholder_bits.append(action.type.__name__)
        if action.nargs in ("*", "+"):
            placeholder_bits.append("mehrere Werte, leerzeichengetrennt")
        if placeholder_bits:
            edit.setPlaceholderText(" / ".join(placeholder_bits))
        return FieldWidget(action, edit, "text")

    def build_argv(self) -> List[str]:
        argv: List[str] = []
        positionals: List[FieldWidget] = []
        optionals: List[FieldWidget] = []
        for f in self.fields:
            (positionals if not f.action.option_strings else optionals).append(f)

        missing = [f for f in self.fields if f.is_required_but_empty()]
        if missing:
            names = ", ".join(
                "/".join(f.action.option_strings) if f.action.option_strings else f.action.dest for f in missing
            )
            raise ValueError(f"Pflichtfelder fehlen: {names}")

        for f in positionals:
            argv.extend(f.to_argv())
        for f in optionals:
            argv.extend(f.to_argv())
        return argv


# --------------------------------------------------------------------------
# 3) Hauptfenster
# --------------------------------------------------------------------------


class MainWindow(QMainWindow):
    def __init__(self, script):
        super().__init__()

        self.pythonscript = script

        self.setWindowTitle("argparse GUI-Runner")
        self.resize(850, 950)

        self.script_path: Optional[str] = None
        self.parser: Optional[argparse.ArgumentParser] = None
        self.form_builder: Optional[ArgFormBuilder] = None
        self.process: Optional[QProcess] = None

        self._build_ui()

    # ---------------------------------------------------------------- UI --
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)

        # Datei wählen
        top_box = QGroupBox("Zielskript")
        top_layout = QHBoxLayout(top_box)
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText(self.pythonscript)
        browse_btn = QPushButton("Durchsuchen...")
        browse_btn.clicked.connect(self._browse_script)
        load_btn = QPushButton("Laden")
        load_btn.clicked.connect(self._load_script)
        top_layout.addWidget(self.path_edit, 1)
        top_layout.addWidget(browse_btn)
        top_layout.addWidget(load_btn)
        outer.addWidget(top_box)

        splitter = QSplitter(Qt.Vertical)
        outer.addWidget(splitter, 1)

        # Formularbereich (scrollbar)
        self.form_scroll = QScrollArea()
        self.form_scroll.setWidgetResizable(True)
        self.form_placeholder = QLabel(
            "Noch kein Skript geladen.\nWähle eine .py-Datei mit argparse und klicke auf 'Laden'."
        )
        self.form_placeholder.setAlignment(Qt.AlignCenter)
        self.form_placeholder.setStyleSheet("color: #888; padding: 30px;")
        self.form_scroll.setWidget(self.form_placeholder)
        splitter.addWidget(self.form_scroll)

        # Run-Leiste
        run_box = QWidget()
        run_layout = QHBoxLayout(run_box)
        self.cmd_preview = QLineEdit()
        self.cmd_preview.setReadOnly(True)
        self.cmd_preview.setPlaceholderText("Befehlsvorschau erscheint hier")
        self.run_btn = QPushButton("▶ Ausführen")
        self.run_btn.clicked.connect(self._run_script)
        self.run_btn.setEnabled(False)
        self.stop_btn = QPushButton("■ Stoppen")
        self.stop_btn.clicked.connect(self._stop_script)
        self.stop_btn.setEnabled(False)
        run_layout.addWidget(QLabel("Befehl:"))
        run_layout.addWidget(self.cmd_preview, 1)
        run_layout.addWidget(self.run_btn)
        run_layout.addWidget(self.stop_btn)
        outer.addWidget(run_box)

        # Log-Bereich
        log_box = QGroupBox("Ausgabe")
        log_layout = QVBoxLayout(log_box)
        self.log_view = TerminalPlainTextEdit()
        self.log_view.line_entered.connect(self._send_input)
        self.log_view = TerminalPlainTextEdit()
        self.log_view.line_entered.connect(self._send_input)
        mono = QFont("Monospace")
        mono.setStyleHint(QFont.TypeWriter)
        self.log_view.setFont(mono)
        log_layout.addWidget(self.log_view)
        splitter.addWidget(log_box)
        splitter.setSizes([320, 350])

        self.statusBar().showMessage("Bereit.")

    # ----------------------------------------------------------- Laden ----
    def _browse_script(self):
        path, _ = QFileDialog.getOpenFileName(self, "Python-Skript wählen", "", "Python-Dateien (*.py)")
        if path:
            self.path_edit.setText(path)

    def _load_script(self):
        path = self.path_edit.text().strip()
        if not path or not os.path.isfile(path):
            # set default path
            path = self.pythonscript
        #            QMessageBox.warning(self, "Fehler", "Bitte einen gültigen Skriptpfad angeben.")
        #            return
        try:
            parser = extract_parser(path)
        except Exception as e:
            QMessageBox.critical(self, "Parser konnte nicht extrahiert werden", str(e))
            return

        self.script_path = path
        self.parser = parser
        self.form_builder = ArgFormBuilder(parser)
        form_widget = self.form_builder.build()

        # Live-Vorschau bei jeder Änderung aktualisieren
        for f in self.form_builder.fields:
            w = f.widget
            if isinstance(w, QCheckBox):
                w.stateChanged.connect(self._update_preview)
            elif isinstance(w, QComboBox):
                w.currentTextChanged.connect(self._update_preview)
            elif isinstance(w, QLineEdit):
                w.textChanged.connect(self._update_preview)

        self.form_scroll.setWidget(form_widget)
        self.run_btn.setEnabled(True)
        self.statusBar().showMessage(
            f"Geladen: {os.path.basename(path)} " f"({len(self.form_builder.fields)} Argument(e) gefunden)", 5000
        )
        self._update_preview()

    # ------------------------------------------------------- Vorschau ----
    def _update_preview(self, *_):
        if not self.form_builder:
            return
        try:
            argv = self.form_builder.build_argv()
            self.cmd_preview.setStyleSheet("")
        except ValueError as e:
            self.cmd_preview.setText(str(e))
            self.cmd_preview.setStyleSheet("color: #b00;")
            return
        cmd = [sys.executable, self.script_path, *argv]
        self.cmd_preview.setText(" ".join(shlex.quote(c) for c in cmd))

    # --------------------------------------------------------- Ausführen ----
    def _run_script(self):
        if not self.form_builder or not self.script_path:
            return
        try:
            argv = self.form_builder.build_argv()
        except ValueError as e:
            QMessageBox.warning(self, "Pflichtfelder fehlen", str(e))
            return

        self.log_view.clear()
        self.log_view.append_output(f"$ {sys.executable} {self.script_path} {' '.join(argv)}\n")
        self.log_view.append_output(f"$ {sys.executable} {self.script_path} {' '.join(argv)}\n")

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self._on_output)
        self.process.finished.connect(self._on_finished)
        self.process.start(sys.executable, [self.script_path, *argv])

        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_view.set_input_enabled(True)
        self.log_view.setFocus()
        self.log_view.set_input_enabled(True)
        self.log_view.setFocus()
        self.statusBar().showMessage("Läuft ...")

    def _on_output(self):
        if self.process:
            data = bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace")
            self.log_view.append_output(data)
            self.log_view.append_output(data)

    def _on_finished(self, exit_code, _exit_status):
        self.log_view.set_input_enabled(False)
        self.log_view.append_output(f"\n[Prozess beendet mit Exit-Code {exit_code}]\n")
        self.log_view.set_input_enabled(False)
        self.log_view.append_output(f"\n[Prozess beendet mit Exit-Code {exit_code}]\n")
        self.run_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.statusBar().showMessage(f"Fertig (Exit-Code {exit_code})", 5000)

    def _send_input(self, line: str):
        """Im Terminal eingegebene Zeile an stdin des Subprozesses senden."""
        if self.process and self.process.state() == QProcess.Running:
            self.process.write((line + "\n").encode("utf-8"))

    def _send_input(self, line: str):
        """Im Terminal eingegebene Zeile an stdin des Subprozesses senden."""
        if self.process and self.process.state() == QProcess.Running:
            self.process.write((line + "\n").encode("utf-8"))

    def _stop_script(self):
        if self.process:
            self.process.kill()
        self.log_view.set_input_enabled(False)
        self.log_view.set_input_enabled(False)


def main():
    # set (default) input file
    if len(sys.argv) > 1:
        script = sys.argv[1]
    else:
        script = default_script

    print(f" script {sys.argv[0]}: wrapping {script} with GUI ...")
    app = QApplication(sys.argv)
    win = MainWindow(script)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":  # --------------------------------------
    default_script = "scGammaDetector.py"
    main()
    
