from configuration_managers.integration_configurator import IntegrationConfigurator

class Eq3BtSmart(IntegrationConfigurator):
    def exists(self) -> bool:
        return self._entry.getDescription(9) == "Complete Local Name"
    
    def get_configuration(self) -> str:
        return '{'
                '"name":"Livingroom",'
                '"mode_cmd_t":"{prefex}/climate/{node}/{obj}/thermostatModeCmd",'
                '"mode_stat_t":"{prefex}/climate/{node}/{obj}/state",'
                '"mode_stat_tpl":"",'
                '"avty_t":"{prefex}/climate/{node}/{obj}/available",'
                '"pl_avail":"online",'
                '"pl_not_avail":"offline",'
                '"temp_cmd_t":"{prefex}/climate/{node}/{obj}/targetTempCmd",'
                '"temp_stat_t":"{prefex}/climate/{node}/{obj}/state",'
                '"temp_stat_tpl":"",'
                '"curr_temp_t":"{prefex}/climate/{node}/{obj}/state",'
                '"curr_temp_tpl":"",'
                '"min_temp":"15",'
                '"max_temp":"25",'
                '"temp_step":"0.5",'
                '"modes":["off", "heat"]'
                '}"'.format(prefex = self._prefex,\
                    node = self._node,\
                    obj = self._entry.addr.replace(":", ""))

