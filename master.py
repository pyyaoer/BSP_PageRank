import socket
import bsp_tr as tr

port = 9000
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8081))
tr.send_file(sock, 'hehe.txt', 0)

s.close()