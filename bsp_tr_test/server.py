import socket
import bsp_tr

port = 8081
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

newsock, address = s.accept()
bsp_tr.get_file(newsock, "new_file.txt")
