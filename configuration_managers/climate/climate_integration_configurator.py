import time, json
from bluepy.btle import ScanEntry
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from configuration_managers.integration_configurator import IntegrationConfigurator

class ClimateIntegrationConfigurator(IntegrationConfigurator):
    def __init__(self, prefix, ip, entry):
        IntegrationConfigurator.__init__(self, prefix, ip, entry)

    def configure(self, config):
        super(ClimateIntegrationConfigurator, self).configure(config)
        hvac_modes = self._device.hvac_modes
        topic = "{prefix}/climate/{node}/{obj}/config".format(prefix = self._prefix, node = self._node, obj = self._object)
        payload_template = {
            "name":"{obj}",
            "unique_id":"{obj}",
            "mode_cmd_t":"{prefix}/climate/{node}/{obj}/mode_cmd_t",
            "mode_stat_t":"{prefix}/climate/{node}/{obj}/state",
            "mode_stat_tpl":"{{{{ value_json.mode }}}}",
            "avty_t":"{prefix}/climate/{node}/{obj}/available",
            "pl_avail":"online",
            "pl_not_avail":"offline",
            "temp_cmd_t":"{prefix}/climate/{node}/{obj}/temp_cmd_t",
            "temp_stat_t":"{prefix}/climate/{node}/{obj}/state",
            "temp_stat_tpl":"{{{{ value_json.target_temp }}}}",
            "curr_temp_t":"{prefix}/climate/{node}/{obj}/state",
            "curr_temp_tpl":"{{{{ value_json.current_temp }}}}",
            "min_temp":self._device.min_temp,
            "max_temp":self._device.max_temp,
            "temp_step":self._device.precision,
            "modes":self._device.hvac_modes
            }
        payload_template_json = "{" + json.dumps(payload_template) + "}"
        print("payload_template_json: ", payload_template_json)
        payload = payload_template_json.format(prefix = self._prefix, node = self._node, obj = self._object)
        print("payload: ", payload)
        self._mqttc.publish(topic, payload=payload, qos=1, retain=False)
        self.subscribe("{prefix}/climate/{node}/{obj}/mode_cmd_t".format(prefix = self._prefix, node = self._node, obj = self._object))
        self.subscribe("{prefix}/climate/{node}/{obj}/temp_cmd_t".format(prefix = self._prefix, node = self._node, obj = self._object))

    def refresh(self):
        self.device.update()
        topic = "{prefix}/climate/{node}/{obj}/available".format(prefix = self._prefix, node = self._node, obj = self._object)
        print("topic: ", topic)
        print("payload: online")
        self._mqttc.publish(topic, payload="online", qos=1, retain=False)

        topic = "{prefix}/climate/{node}/{obj}/state".format(prefix = self._prefix, node = self._node, obj = self._object)
        payload = self.device.device_state_attributes
        payload["mode"] = self.device.hvac_mode
        payload["target_temp"] = self.device.target_temperature
        payload["current_temp"] = self.device.current_temperature
        payload_json = json.dumps(payload)
        print("topic: ", topic)
        print("payload: ", payload_json)
        self._mqttc.publish(topic, payload=payload_json, qos=1, retain=False)
