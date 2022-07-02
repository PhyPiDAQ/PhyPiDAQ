import collections

import numpy as np
import paho.mqtt.client as mqtt


class TelematicsConfig:

    def __init__(self, confdict=None):

        # Initialize internal properties
        self.connected = False
        # Limit the size of the queue to limit memory usage
        self.queue = collections.deque([], maxlen=1000)

        self.publish_topic = "Steuerung"

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

        # Create instance of client and give him a random client id
        self.client = mqtt.Client(clean_session=False)

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

        # Start data acquisition
        self.client.publish(self.publish_topic, "start", qos=1)

    def _on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        value_list = message.split(" ")
        # Convert the first item of the list to a double and append to the internal queue
        self.queue.append(np.double(value_list[0]))

    def acquireData(self, buf):
        # Skip, if there is no data in the queue
        if len(self.queue) == 0:
            pass
        elif self.connected:
            # Return the first element of the list
            buf[0] = self.queue.popleft()
        else:
            pass

    def closeDevice(self):
        self.client.publish(self.publish_topic, "stopp", qos=1)
        self.queue.clear()
        self.connected = False
        self.client.loop_stop()
        self.client.disconnect()
