import socket, sys, json, time, sched
from collections import namedtuple
import netifaces as ni
from bluepy.btle import Scanner, ScanEntry 

from configuration_managers.climate.eq3btsmart import Eq3BtSmartConfig
from multiprocessing import Queue

PORT = 35224
devices = []

def start_tcp_discovery(queue: Queue):
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (ip, PORT)
    print("starting up on %s port %s" % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    scanner = Scanner()

    while True:
        # Wait for a connection
        print("waiting for a connection")
        connection, client_address = sock.accept()

        try:
            print("connection from", client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1024)
                resp = ""
                print("received '%s'" % data)
                msg = data.decode()
                if msg == 'ha-rpi-bt-ext device discovery':
                    devices = scanner.scan(10.0)

                    for dev in devices:
                        eq3 = Eq3BtSmartConfig("homeassistant", ip, dev)
                        if eq3.exists():
                            resp +=";" + dev.addr + "-" + str(dev.rssi) + ";"

                        # eq3 = False
                        # for (adtype, desc, value) in dev.getScanData():
                        #     if desc == "Complete Local Name" and value == "CC-RT-BLE":
                        #         eq3 = True
                        #         break
                        # if eq3:
                        #     resp += dev.addr + ":" + str(dev.rssi) + ";"
                    print("sending data back to the client")
                    print("data:", resp[:-1])
                    connection.sendall((resp[:-1]).encode())
                    queue.put("")
                elif msg.startswith('ha-rpi-bt-ext device configure:'):
                    queue.put(msg[msg.index(":") + 1:])
                    connection.sendall(b'ha-rpi-bt-ext device configured')
                else:
                    print("no more data from", client_address)
                    break
        except ConnectionResetError:
            continue
        finally:
            # Clean up the connection
            connection.close()
