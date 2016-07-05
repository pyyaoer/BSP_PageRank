import socket
import bsp_cm as cm
import bsp_dg as dg
import bsp_tr as tr

port = 9000
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

# divide the graph and generates the partition txt
node_list = {}
node_list[1] = ("localhost", 8001, False)
dg.divide_graph("wiki-Vote.txt", 3)

for key in node_list:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((node_list[key][0], node_list[key][1]))
	tr.send_file(sock, 'hehe.txt', 0)

while True:
	if cm.wait_slaves():
		break

s.close()