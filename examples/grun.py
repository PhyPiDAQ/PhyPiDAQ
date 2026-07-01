#!/usr/bin/env python3
"""
argparse GUI-Runner
====================
Lädt ein beliebiges Python-Skript, das `argparse` verwendet, extrahiert
dessen ArgumentParser (ohne das Skript "richtig" laufen zu lassen) und
baut daraus automatisch ein Eingabeformular. Beim Klick auf "Ausführen"
wird das Original-Skript als Subprozess mit den eingegebenen Parametern
gestartet; die Ausgabe erscheint im Terminalfenster, aus dem grun.py
ausgeführt wurde.

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
import subprocess

from PyQt5.QtCore import Qt, QProcess

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
    QGroupBox,
    QSplitter,
    QMessageBox,
    QFileDialog,
    QScrollArea,
)

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
        self.resize(600, 750)

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
        run_layout.addWidget(QLabel("Befehl:"))
        run_layout.addWidget(self.cmd_preview, 1)
        run_layout.addWidget(self.run_btn)
        outer.addWidget(run_box)

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

        cmd = ["python3", self.script_path]
        arg_lst = cmd + argv
        cmd_str = " ".join(shlex.quote(a) for a in arg_lst)
        print("Starte ", cmd_str)
        self.proc = subprocess.run(arg_lst)


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
