import time
from bluepy.btle import ScanEntry
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from configuration_managers.integration_configurator import IntegrationConfigurator

class ClimateIntegrationConfigurator(IntegrationConfigurator):
    def __init__(self, prefix, ip, entry):
        IntegrationConfigurator.__init__(self, prefix, ip, entry)

    def configure_over_mqtt(self):
        topic = "{prefix}/climate/{node}/{obj}/config".format(prefix = self._prefix, node = self._node, obj = self._object)
        payload_template = {
            "name":"{obj}",
            "unique_id":"{obj}"
            "mode_cmd_t":"{prefix}/climate/{node}/{obj}/mode_cmd_t",
            "mode_stat_t":"{prefix}/climate/{node}/{obj}/state",
            "mode_stat_tpl":"{{ value_json.mode }}",
            "avty_t":"{prefix}/climate/{node}/{obj}/available",
            "pl_avail":"online",
            "pl_not_avail":"offline",
            "temp_cmd_t":"{prefix}/climate/{node}/{obj}/targetTempCmd",
            "temp_stat_t":"{prefix}/climate/{node}/{obj}/state",
            "temp_stat_tpl":"{{ value_json.target_temp }}",
            "curr_temp_t":"{prefix}/climate/{node}/{obj}/state",
            "curr_temp_tpl":"{{ value_json.curr_temp }}",
            "min_temp":"15",
            "max_temp":"25",
            "temp_step":"0.5",
            "modes":["off", "heat"]
            }
        payload_template_json = json.dumps(payload_template)
        payload = payload_template_json.format(prefix = self._prefix, node = self._node, obj = self._object)
        self._mqttc.publish(topic, payload=payload, qos=1, retain=False)

    def refresh(self):
        self.device.update()
        topic = "{prefix}/climate/{node}/{obj}/state".format(prefix = self._prefix, node = self._node, obj = self._object)
        payload = {}
        payload["mode"] = self.device.hvac_mode
        payload["target_temp"] = self.device.target_temperature
        payload["current_temp"] = self.device.current_temperature
        self._mqttc.publish(topic, payload=payload, qos=1, retain=False)