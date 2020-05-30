from configuration_managers.integration_configurator import IntegrationConfigurator
import paho.mqtt.client as mqtt

class Eq3BtSmart(IntegrationConfigurator):
    def exists(self) -> bool:
        return self._entry.getValueText(9) == "CC-RT-BLE"
    
    def configure(self, config):
        super(Eq3BtSmart, self).configure(config)

        topic = "{prefix}/climate/{node}/{obj}/config".format(prefix = self._prefix, node = self._node, obj = self._object)
        payload_template = '''{{
"name":"{obj}",
"unique_id":"{obj}",
"mode_cmd_t":"{prefix}/climate/{node}/{obj}/thermostatModeCmd",
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
}}'''
        payload = payload_template.format(prefix = self._prefix, node = self._node, obj = self._object)
        super(Eq3BtSmart, self).configure_device_delayed(topic, payload, 1, False)

