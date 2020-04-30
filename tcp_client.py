import socket
import sys
import netifaces as ni

PORT = 35224
ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (ip, PORT)
print("starting up on %s port %s" % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print("waiting for a connection")
    connection, client_address = sock.accept()

    try:
        print("connection from", client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print("received '%s'" % data)
            if data:
                print("sending data back to the client")
                connection.sendall(data)
            else:
                print("no more data from", client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
