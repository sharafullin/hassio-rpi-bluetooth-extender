import time
from bluepy.btle import ScanEntry
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

class IntegrationConfigurator:
    def __init__(self, prefix, ip, entry):
        self._entry = entry
        self._node = ip.replace(".","_")
        self._object = entry.addr.replace(":","")
        self._prefix = prefix
        self._mqttc = mqtt.Client(self._object)
        self._callbacks = {}

    def exists(self) -> bool:
        pass

    def configure(self, config):
        self._mqtt_username = config.username
        self._mqtt_password = config.password
        self._mqtt_broker = config.broker
        self._mqtt_port = config.port

        self._mqttc.username_pw_set(config.username, config.password)

        self._mqttc.on_message = self._mqtt_on_message

        self._mqttc.connect(config.broker, int(config.port), 60)
        self._mqttc.loop_start()
        print("loop started")

    def refresh(self):
        pass


    @property
    def device(self):
        return self._device

    def subscribe(self, topic, callback):
        print("subscribed for: ", topic)
        self._mqttc.subscribe(topic)
        self._callbacks[topic] = callback

    def _mqtt_on_message(self, _mqttc, _userdata, msg) -> None:
        """Message received callback."""
        print("Command. Topic: ", msg.topic)
        print("Command. Payload: ", msg.payload.decode())
        self._callbacks[msg.topic](msg.payload)
        print("refresh")
        self.refresh()
