import sys
import socket
import bsp_lc as lc
import bsp_cm as cm
import bsp_bs as bs
import bsp_tr as tr


port = int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

master_port = 9000
master_host = "127.0.0.1"

while True:
	while True:
		sock, addr = s.accept()
		node_id = tr.get_file(sock, "master.txt")
		if (int(node_id) == 0):
			break
	break

s.close()