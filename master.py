import socket
import bsp_tr as tr

port = 9000
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

s.close()