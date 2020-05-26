from multiprocessing import Process
import udp_discovery
import tcp_discovery
import delayed

udp_discovery_process = Process(target=udp_discovery.start_udp_discovery)
udp_discovery_process.start()

tcp_discovery_process = Process(target=tcp_discovery.start_tcp_discovery)
tcp_discovery_process.start()

delayed_process = Process(target=delayed.start_task_processing)
delayed_process.start()

udp_discovery_process.join()
tcp_discovery_process.join()
delayed_process.join()
