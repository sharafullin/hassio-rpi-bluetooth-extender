from multiprocessing import Process
import udp_discovery
import tcp_discovery

udp_discovery_process = Process(target=udp_discovery.start_udp_discovery)
udp_discovery_process.start()

tcp_discovery_process = Process(target=tcp_discovery.start_tcp_discovery)
tcp_discovery_process.start()

udp_discovery_process.join()