from multiprocessing import Process, Queue
import udp_discovery
import tcp_discovery
import delayed_queue
from configuration_managers.integration_configurator import IntegrationConfigurator
import time, sched, json
from collections import namedtuple
from bluepy.btle import Scanner, ScanEntry 

q = Queue()
scanner = Scanner()

def heartbeat():
    print(time.time(), "heartbeat")

    while not q.empty():
        data = q.get(timeout=0.5)
        config = data.split("__")
        mqtt_conf = json.loads(config[1], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        print("dev mac:", config[0])
        print("dev config:", config[1])
        devices = scanner.scan(3.0)
        for device in devices:
            if device.addr == config[0]:
                eq3 = Eq3BtSmart("homeassistant", ip, device)
                eq3.configure(mqtt_conf)
    s.enter(3, 1, heartbeat)

s = sched.scheduler(time.time, time.sleep)
s.enter(3, 1, heartbeat)

udp_discovery_process = Process(target=udp_discovery.start_udp_discovery)
udp_discovery_process.start()

tcp_discovery_process = Process(target=tcp_discovery.start_tcp_discovery, args=(q,))
tcp_discovery_process.start()

delayed_process = Process(target=delayed_queue.start_task_processing)
delayed_process.start()


s.run()

udp_discovery_process.join()
tcp_discovery_process.join()
delayed_process.join()

