import socket
import select

sock = socket.socket()
sock.bind(('', 10001))
sock.listen()

conn1, addr = sock.accept()
conn2, addr = sock.accept()

conn1.setblocking(False)
conn2.setblocking(False)

epoll = select.epoll()