import socket
import bsp_cm as cm
import bsp_dg as dg
import bsp_tr as tr

node_list = {}
node_list[1] = ("localhost", 8001)
node_list[2] = ("localhost", 8002)

port = 9000
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

# divide the graph and generates the partition txt
node_num = len(node_list)
node_adj = dg.divide_graph("wiki-Vote.txt", node_num)

# send partition infomation to slaves
for key in node_list:
	#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock.connect((node_list[key][0], node_list[key][1]))
	#tr.send_file(sock, "task_"+str(key)+".txt", key)
	print "task_"+str(key)+".txt"

while True:
	node_report_num = 0
	while node_num != node_report_num:
		#sock, addr = s.accept()
		#node_id = int(tr.get_file(sock, "report_" + str(node_report_num+1) + ".txt"))
		print "report_" + str(node_report_num+1) + ".txt"
		node_report_num = node_report_num + 1
	break

s.close()