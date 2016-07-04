import sys
import socket
import bsp_lc as lc
import bsp_cm as cm
import bsp_bs as bs
import bsp_tr as tr

def build_adjnodes():
	return []

port = int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

master_port = 9000
master_host = "127.0.0.1"

while True:
	# if the adjacent node has sent the message
	adjacent_nodes = {}
	while True:
		sock, addr = s.accept()
		node_id = int(tr.get_file(sock, "master.txt"))
		if (node_id == 0):
			n_list = build_adjnodes()
			for key in n_list:
				if not adjacent_nodes.has_key(key):
					adjacent_nodes[key] = False
			break
		adjacent_nodes[node_id] = True
	lc.local_compute()
	cm.send_messages()
	cm.wait_messages()
	bs.barrier_sync()
	break

s.close()