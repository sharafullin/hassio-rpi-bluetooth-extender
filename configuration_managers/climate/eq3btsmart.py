import json
from configuration_managers.integration_configurator.climate import ClimateIntegrationConfigurator
import paho.mqtt.client as mqtt
from integrations.climate.eq3btsmart.climate import EQ3BTSmartThermostat

class Eq3BtSmartConfig(ClimateIntegrationConfigurator):
    def __init__(self, prefix, ip, entry):
        ClimateIntegrationConfigurator.__init__(self, prefix, ip, entry)
        self._device = EQ3BTSmartThermostat(self._entry.addr, self._entry.addr)

    def exists(self) -> bool:
        return self._entry.getValueText(9) == "CC-RT-BLE"
    
    def configure(self, config):
        super(Eq3BtSmartConfig, self).configure(config)


