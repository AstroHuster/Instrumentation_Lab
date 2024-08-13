""" server.py
"""
from connect import wlan
import socket
import machine

address = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)
s.listen(1)
print("Listening for connection on ", wlan.ifconfig()[0])

response = """<!DOCTYPE html>
<html>
<head>
  <title>Pico W</title>
</head>
<body>
  <h1>Pico W</h1>
  <p>Hello World</p>
</body>
</html>
"""
while True:
    try:
        client, address = s.accept()
        print("Connection accepted from ", address)
        client_file = client.makefile("rwb", 0)
        while True:
            line = client_file.readline()
            if not line or line == b"\r\n":
                break

        client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        client.send(response)
        client.close()
        print("Response sent, connection closed.")
    except OSError as e:
        client.close()
        print("Error, connection closed")

# End Of File
