import socket
import sys
import json
import netifaces as ni
from bluepy.btle import Scanner, ScanEntry 

from configuration_managers.climate.eq3btsmart import Eq3BtSmart

PORT = 35224
devices = []

def start_tcp_discovery():
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
                    devices = scanner.scan(3.0)

                    for dev in devices:
                        print("device:")
                        print(dev)
                        eq3 = Eq3BtSmart("homeassistant", ip, dev)
                        if eq3.exists():
                            print("exists")
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
                elif msg.startswith('ha-rpi-bt-ext device configure'):
                    config = msg.split("__")
                    mqtt_conf = json.loads(config[2], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                    print("configuring the device: ", config[1])
                    for dev in devices:
                        if dev.addr == config[1]:
                            device = dev
                    eq3 = Eq3BtSmart("homeassistant", ip, device)
                    if eq3.exists():
                        eq3.configure(config[2])
                    connection.sendall(b'ha-rpi-bt-ext device configured')
                else:
                    print("no more data from", client_address)
                    break
        except ConnectionResetError:
            continue
        finally:
            # Clean up the connection
            connection.close()
