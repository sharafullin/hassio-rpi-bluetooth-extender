from multiprocessing import Process
import udp_discovery
import tcp_discovery
import delayed_queue

import time, sched

def heartbeat():
    print(time.time(), "heartbeat")

    s.enter(3, 1, heartbeat)

s = sched.scheduler(time.time, time.sleep)
s.enter(3, 1, heartbeat)

udp_discovery_process = Process(target=udp_discovery.start_udp_discovery)
udp_discovery_process.start()

tcp_discovery_process = Process(target=tcp_discovery.start_tcp_discovery, args=(s,))
tcp_discovery_process.start()

delayed_process = Process(target=delayed_queue.start_task_processing)
delayed_process.start()


s.run()

udp_discovery_process.join()
tcp_discovery_process.join()
delayed_process.join()

