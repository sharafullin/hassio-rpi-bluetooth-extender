from bluepy.btle import ScanEntry 

class IntegrationConfigurator:
    def __init__(self, prefix, ip, entry):
        self._entry = entry
        self._node = ip.replace(".","_")
        self._object = entry.addr.replace(":","")
        self._prefix = prefix

    def exists(self) -> bool:
        pass

    def configure(self) -> str:
        pass
