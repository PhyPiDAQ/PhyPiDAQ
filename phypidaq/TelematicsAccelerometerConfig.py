import collections
import time
import uuid
import numpy as np
import paho.mqtt.client as mqtt


class TelematicsAccelerometerConfig:

    def __init__(self, confdict=None):

        # Initialize internal properties
        self.connected = False
        self.last_time = time.time()
        # Limit the size of the queue to limit memory usage
        self.queue = collections.deque([], maxlen=1000)

        if confdict is None:
            confdict = {}

        if "ip_address" in confdict:
            self.ip_address = confdict["ip_address"]
        else:
            self.ip_address = "127.0.0.1"

        if "port" in confdict:
            self.port = confdict["port"]
        else:
            self.port = 1883

        if "subscribe_topic" in confdict:
            self.subscribe_topic = confdict["subscribe_topic"]
        else:
            self.subscribe_topic = "ms2"

        if "publish_topic" in confdict:
            self.publish_topic = confdict["publish_topic"]
        else:
            self.publish_topic = "Steuerung"

        if "control_topic" in confdict:
            self.control_topic = confdict["control_topic"]
        else:
            self.control_topic = "Abtastrate"

        if "interval" in confdict:
            self.interval = confdict["interval"]
            # Ensure that the interval is in a matching range
            if self.interval < 0.01:
                self.interval = 0.1
        else:
            self.interval = 0.1

        if "Channels" in confdict:
            if isinstance(confdict["Channels"], list):
                self.channels = confdict["Channels"]
                # Ensure, that all items are lowercase
                self.channels = [x.lower() for x in self.channels]
                # Filter list, to keep only valid channels
                self.channels = [x for x in self.channels if x in ["x", "y", "z"]]
                # Check if enough channels are listed
                if len(self.channels) < 1:
                    # Set only one channel
                    print("No valid channels have been specified! Resetting it to following channels: x")
                    self.channels = ["x"]
            else:
                # Support only one channel
                self.channels = ["x"]
        else:
            # Support only one channel
            self.channels = ["x"]

        # Calculate NChannels and limits
        self.NChannels = len(self.channels)
        self.ChanLims = self.NChannels * [[-4., 4.]]
        self.ChanNams = self.NChannels * ["Acceleration"]
        # Acceleration in g (9.81 m/s^2)
        self.ChanUnits = self.NChannels * ["g"]

        # Create instance of client and give him a random client id
        self.client = mqtt.Client("PhyPiDAQ-client-" + str(uuid.uuid1()), clean_session=False)

        # Register the client callbacks
        self.client.on_connect = self._connect
        self.client.on_message = self._on_message

    def init(self):
        # Try connecting to the client
        self.client.connect(self.ip_address, self.port)

        # Start the data acquisition loop
        self.client.loop_start()

    def _connect(self, client, userdata, flags, rc):
        # Update the connected status
        self.connected = True
        # Once the client has connected to the broker, subscribe to the topic
        if len(self.subscribe_topic.strip()) != 0:
            self.client.subscribe(self.subscribe_topic)

        # Publish the data acquisition interval
        self.client.publish(self.control_topic, round(self.interval * 1000), qos=1)

        # Start data acquisition
        self.client.publish(self.publish_topic, "start", qos=1)

    def _on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        value_list = message.split(" ")

        # If it's time to add the new value, do it
        current_time = time.time()
        if current_time >= self.interval + self.last_time:
            # Convert the first item of the list to a double and append to the internal queue
            if len(value_list) < 3:
                raise AttributeError("Array hasn't required size")
            # This is considered to be: 0 -> x, 1 -> y, 2 -> z
            self.queue.append([np.double(value_list[0]), np.double(value_list[1]), np.double(value_list[2])])
            self.last_time = current_time

    def acquireData(self, buf):
        # Skip, if there is no data in the queue
        if len(self.queue) == 0:
            pass
        elif self.connected:
            # Return the first element of the list
            data_list = self.queue.popleft()

            # Fill the buffer with the wanted data
            if "x" in self.channels:
                buf[0] = data_list[0]
            if "y" in self.channels:
                if "x" in self.channels:
                    buf[1] = data_list[1]
                else:
                    buf[0] = data_list[1]
            if "z" in self.channels:
                if "x" in self.channels and "y" in self.channels:
                    buf[2] = data_list[2]
                elif "x" in self.channels or "y" in self.channels:
                    buf[1] = data_list[2]
                else:
                    buf[0] = data_list[2]
        else:
            pass

    def closeDevice(self):
        self.client.publish(self.publish_topic, "stopp", qos=1)
        self.queue.clear()
        self.connected = False
        self.client.loop_stop()
        self.client.disconnect()
