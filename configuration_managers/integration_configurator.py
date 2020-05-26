from bluepy.btle import ScanEntry
import paho.mqtt.client as mqtt
import redis
from delayed.queue import Queue
from delayed.delay import delayed

class IntegrationConfigurator:
    def __init__(self, prefix, ip, entry):
        self._entry = entry
        self._node = ip.replace(".","_")
        self._object = entry.addr.replace(":","")
        self._prefix = prefix
        self._mqttc = mqtt.Client(protocol=mqtt.MQTTv311)

    def exists(self) -> bool:
        pass

    def configure_device_delayed(self, topic, payload, qos, retain):
        conn = redis.Redis()
        queue = Queue(name='default', conn=conn)
        delayed = delayed(queue)

        self.configure_device.timeout(10)(IntegrationConfigurator, topic, payload, qos, retain)

    @delayed()
    def configure_device(self, topic, payload, qos, retain):
        self._mqttc.publish(topic, payload, qos, retain)

    def configure(self, config):
        self._mqttc.username_pw_set(config.username, config.password)

        self._mqttc.on_connect = self._mqtt_on_connect
        self._mqttc.on_disconnect = self._mqtt_on_disconnect
        self._mqttc.on_message = self._mqtt_on_message

        self._mqttc.connect(config.broker, config.port, True)

        print('mqtt connected!')

    def _mqtt_on_connect(self, _mqttc, _userdata, _flags, result_code: int) -> None:
        """On connect callback.

        Resubscribe to all topics we were subscribed to and publish birth
        message.
        """

        if result_code != mqtt.CONNACK_ACCEPTED:
            _LOGGER.error(
                "Unable to connect to the MQTT broker: %s",
                mqtt.connack_string(result_code),
            )
            self._mqttc.disconnect()
            return

        self.connected = True

        # Group subscriptions to only re-subscribe once for each topic.
        keyfunc = attrgetter("topic")
        for topic, subs in groupby(sorted(self.subscriptions, key=keyfunc), keyfunc):
            # Re-subscribe with the highest requested qos
            max_qos = max(subscription.qos for subscription in subs)
            self.hass.add_job(self._async_perform_subscription, topic, max_qos)

        if self.birth_message:
            self.hass.add_job(
                self.async_publish(  # pylint: disable=no-value-for-parameter
                    *attr.astuple(
                        self.birth_message,
                        filter=lambda attr, value: attr.name != "subscribed_topic",
                    )
                )
            )

    def _mqtt_on_message(self, _mqttc, _userdata, msg) -> None:
        """Message received callback."""
        self.hass.add_job(self._mqtt_handle_message, msg)

    def _mqtt_on_disconnect(self, _mqttc, _userdata, result_code: int) -> None:
        """Disconnected callback."""
        self.connected = False

        # When disconnected because of calling disconnect()
        if result_code == 0:
            return

        tries = 0

        while True:
            try:
                if self._mqttc.reconnect() == 0:
                    self.connected = True
                    _LOGGER.info("Successfully reconnected to the MQTT server")
                    break
            except OSError:
                pass

            wait_time = min(2 ** tries, MAX_RECONNECT_WAIT)
            _LOGGER.warning(
                "Disconnected from MQTT (%s). Trying to reconnect in %s s",
                result_code,
                wait_time,
            )
            # It is ok to sleep here as we are in the MQTT thread.
            time.sleep(wait_time)
            tries += 1

