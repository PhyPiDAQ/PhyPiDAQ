import multiprocessing as mp
import asyncio
import websockets


class WebsocketManager(object):
    """starts websockets server as background process;
    sends data to websocket on localhost:8314

    sent data can be read with script
    read_Websocket.py ws://localhost:8314
    """

    def __init__(self, interval=0.1, config_dict=None, data_queue=None):
        self.processes = []
        self.data_queue = data_queue
        self.interval = interval
        if config_dict is not None:
            self.config_dict = config_dict
        else:
            self.config_dict = {}

        # Create queue if not set
        if self.data_queue is None:
            # Queue for data transfer to sub-process
            self.data_queue = mp.Queue(1)

        # Create a new process
        self.processes.append(mp.Process(name="WebsocketServer", target=self.spawn_websocket))

        for prc in self.processes:
            # Start all processes, that haven't started yet
            if not prc.is_alive():
                prc.start()
                print('Starting subprocess ', prc.name, ' PID=', prc.pid)

    def __call__(self, dat):
        self.data_queue.put(dat)

    def close(self):
        # Shut-down all sub-process(es)
        for p in self.processes:
            if p.is_alive():
                p.terminate()
                print('Terminating ' + p.name)

    def spawn_websocket(self):
        host = ''
        port = 8314
        dbg = False

        async def data_provider(websocket, path):
            async for message in websocket:
                if dbg:
                    print("server got: ", message)

                if message == "req_connect":
                    # confirm connection
                    await websocket.send("ack_connect")
                else:
                    #  get and send data
                    while True:
                        inp = self.data_queue.get()
                        if dbg:
                            print("sending", inp)
                        await websocket.send(inp)
                        if inp == '\n':
                            if dbg:
                                print("received empty input -> end")
                            break

        # start web service
        print('** server running under uri ws://' + host + ':', port)
        start_server = websockets.serve(data_provider, host, port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
