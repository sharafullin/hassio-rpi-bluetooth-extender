from configuration_managers.integration_configurator import IntegrationConfigurator

class Eq3BtSmart(IntegrationConfigurator):
    def exists(self) -> bool:
        return self._entry.getValueText(9) == "CC-RT-BLE"
    
    def get_configuration(self) -> str:
        result = '''{{
"name":"Livingroom",
"mode_cmd_t":"{prefix}/climate/{node}/{obj}/thermostatModeCmd",
"mode_stat_t":"{prefix}/climate/{node}/{obj}/state",
"mode_stat_tpl":"",
"avty_t":"{prefix}/climate/{node}/{obj}/available",
"pl_avail":"online",
"pl_not_avail":"offline",
"temp_cmd_t":"{prefix}/climate/{node}/{obj}/targetTempCmd",
"temp_stat_t":"{prefix}/climate/{node}/{obj}/state",
"temp_stat_tpl":"",
"curr_temp_t":"{prefix}/climate/{node}/{obj}/state",
"curr_temp_tpl":"",
"min_temp":"15",
"max_temp":"25",
"temp_step":"0.5",
"modes":["off", "heat"],'\
'"rssi":"{rssi}",'\
'"id":"{obj}"'\
}}'''
        return result.format(prefix = self._prefix, node = self._node, obj = self._object, rssi = self._entry.rssi)

