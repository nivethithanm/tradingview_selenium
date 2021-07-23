import socket
import time

HEADER = 64

# Server address

# # Localhost
# SERVER = '3.131.207.170'
# # local-host port
# PORT = 5050

# ngrok public server
# Forwarding                    tcp://4.tcp.ngrok.io:14443 -> localhost:5050
SERVER = socket.gethostbyname('2.tcp.ngrok.io')
# Ngrok public port
PORT = 12447

DISCONNECT_MESSAGE = '!disconnect'
ADDRESS = (SERVER, PORT)

# set up a socket for the client to listen to the server
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# rather than bind we use connect here to connect and establish a communication between server and client
client.connect(ADDRESS)

# send some data to the server


def send(msg):
    # encode the message to bytes
    message = msg.encode('utf-8')
    # we need to set the header of the message
    msg_len = len(message)
    # encode message length to bytes
    message_length = str(msg_len).encode('utf-8')
    padd_length = b' ' * (HEADER - len(message_length))
    final_message_length = message_length+padd_length
    print('sdfghjk')
    # send header
    client.send(final_message_length)
    # send the actual message
    client.send(message)
    time.sleep(5)
    # recieve confirmation from server
    print(client.recv(2048).decode('utf-8'))


print('sdfghjkjhgfd')
# speak with server
send('hello world!')

# close the connection
send(DISCONNECT_MESSAGE)

# what if we wanna send an object or other types instead of string as a message
# 1. we can send message that are json serialised
# 2. we can send it as pickle - u can pickle an entire python object which is a way of serializing it
# the server can unpickle it and use it
