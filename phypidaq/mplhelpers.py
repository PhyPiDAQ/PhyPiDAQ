"""matplotlib helper functions"""

import sys
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = mpl.get_backend()
    if backend == "TkAgg":
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == "WXAgg":
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)


class controlGUI:
    """graphical user interface to control apps via multiprocessing Queue

    Args:

      - cmdQ: a multiprocessing Queue to accept commands
      - appName: name of app to be controlled
      - statQ: mp Queue to show status data
      - confdict: a configuration dictionary for buttons, format {name: [position 0-5, command]}
    """

    def __init__(self, cmdQ, appName="TestApp", statQ=None, confdict=None):
        self.cmdQ = cmdQ
        self.statQ = statQ
        self.button_dict = {'x': [5, ' ']} if confdict is None else confdict
        self.button_names = list(self.button_dict.keys())
        self.button_values = list(self.button_dict.values())

        self.mpl_active = True
        self.interval = 100  # update for timer

        mpl.rcParams['toolbar'] = 'None'
        # create a figure
        self.f = plt.figure("control Gui", figsize=(5.0, 1.0))
        move_figure(self.f, 1200, 0)
        self.f.canvas.mpl_connect("close_event", self.on_mpl_window_closed)

        self.f.subplots_adjust(left=0.025, bottom=0.025, right=0.975, top=0.975, wspace=None, hspace=0.1)
        gs = self.f.add_gridspec(nrows=7, ncols=1)
        # 1st subplot for text
        self.ax0 = self.f.add_subplot(gs[:-2, :])
        # no axes or labels
        self.ax0.xaxis.set_tick_params(labelbottom=False)
        self.ax0.yaxis.set_tick_params(labelleft=False)
        self.ax0.set_xticks([])
        self.ax0.set_yticks([])
        self.ax0.text(0.01, 0.78, "Process control:", size=12)
        self.ax0.text(0.15, 0.45, f"{appName}", color="goldenrod", size=15)
        self.status_txt = self.ax0.text(0.05, 0.1, "", color="ivory")

    # call-back functions
    def on_mpl_window_closed(self, ax):
        # active when application window is closed
        self.mpl_active = False
        self.cmdQ.put("E")
        time.sleep(0.3)
        sys.exit(0)

    def on_button_clicked(self, event):
        # find numer of the clicked button
        b_idx = self.baxes.index(event.inaxes)
        # extract sommand
        cmd = self.button_values[b_idx][1]
        # send to controlled process
        self.cmdQ.put(cmd)

    def cb_end(self, event):
        # active when application window is closed
        self.mpl_active = False
        self.cmdQ.put("E")
        time.sleep(0.3)
        sys.exit(0)

    def update(self, ax):
        """called by timer"""
        if self.statQ and not self.statQ.empty():
            self.status_txt.set_text(self.statQ.get())
        ax.figure.canvas.draw()

    def run(self):
        """run the GUI"""
        # create commad buttons
        self.baxes = []
        self.buttons = []
        for i, key in enumerate(self.button_names):
            self.baxes.append(self.f.add_axes([self.button_values[i][0] * 0.15 + 0.04, 0.05, 0.12, 0.20]))
            self.buttons.append(Button(self.baxes[-1], key, color="0.25", hovercolor="0.5"))
            self.buttons[-1].on_clicked(self.on_button_clicked)

        # timer waking up 10 times/s
        timer = self.f.canvas.new_timer(interval=self.interval)
        timer.add_callback(self.update, self.ax0)
        self.t_start = time.time()
        timer.start()

        print("*==* GUI for process control started")
        plt.show()


def run_controlGUI(*args, **kwargs):
    gui = controlGUI(*args, **kwargs)
    gui.run()
