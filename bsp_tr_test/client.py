import socket
import bsp_tr

port = 8082
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.connect(('localhost', 8081))

bsp_tr.send_file(s, 'hehe.txt')