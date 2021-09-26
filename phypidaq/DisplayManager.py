import multiprocessing as mp
import time

from PyQt5.QtWidgets import QApplication

from phypidaq.Display import Display


class DisplayManager:

    def __init__(self, interval=0.1, config_dict=None, cmd_queue=None, data_queue=None):
        self.processes = []
        self.cmd_queue = cmd_queue
        self.data_queue = data_queue

        self.interval = interval

        if config_dict is not None:
            self.config_dict = config_dict
        else:
            self.config_dict = {}

    def init(self):

        # Create queue if not set
        if self.data_queue is None:
            # Queue for data transfer to sub-process
            self.data_queue = mp.Queue(1)

        # Create a new process
        self.processes.append(mp.Process(name="Display instance", target=self.spawnWindow))

        for prc in self.processes:
            # Start all processes, that haven't started yet
            if not prc.is_alive():
                prc.start()
                print('Starting subprocess ', prc.name, ' PID=', prc.pid)

    def spawnWindow(self):
        app = QApplication([])
        display = Display(self.interval, self.config_dict, self.cmd_queue, self.data_queue)
        display.show()
        app.exec()

    def showData(self, dat):
        # Send data to display process
        self.data_queue.put(dat)
        # Waiting time to make data transfer reliable
        time.sleep(0.00005)

    def close(self):
        # Shut-down all sub-process(es)
        for p in self.processes:
            if p.is_alive():
                p.terminate()
                print('Terminating ' + p.name)
