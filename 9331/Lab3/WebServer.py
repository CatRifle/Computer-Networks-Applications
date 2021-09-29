from socket import *
import sys

host = 'localhost'
port = int(sys.argv[1])

print('\n')
print(f'IP address:{host}')
socket = socket(AF_INET, SOCK_STREAM)
# create a socket for listening request
socket.bind((host, port))
socket.listen(6)

while True:
    # print("\n\nThe server is Ready...")
    # create a socket for TCP connection
    connection, address = socket.accept()
    try:

        request = connection.recv(1024).decode()
        req_file = request.split()[1]

        f = open(req_file[1:], 'rb')
        content = f.read()
        connection.send(b"HTTP/1.1 200 OK\r\n\r\n")
        # send the contend of the file requested by the browser
        connection.send(content)
        connection.close()

    except IOError:
        connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connection.send(b"404 Not Found")
        connection.close()
