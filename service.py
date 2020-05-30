from multiprocessing import Process, Queue
import udp_discovery
import tcp_discovery
import delayed_queue

import time, sched

q = Queue()

def heartbeat():
    print(time.time(), "heartbeat")

    try:
        dev = q.get(timeout=0.5)
        print("dev:", dev)
    except Queue.empty:
        print("empty")

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

