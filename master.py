import os
import socket
import fileinput
import bsp_cm as cm
import bsp_dg as dg
import bsp_tr as tr

ele_list = {}

node_list = {}
node_list[1] = ("localhost", 8001)
node_list[2] = ("localhost", 8002)

port = 9000
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
#s.listen(5)

# divide the graph and generates the partition txt
node_num = len(node_list)
ele_num, node_adj = dg.divide_graph("wiki-Vote.txt", node_num)

# send partition infomation to slaves
for key in node_list:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((node_list[key][0], node_list[key][1]))
	tr.send_file(sock, "task_"+str(key)+".txt", key)
	print "send task file to node "+str(key)

while True:
	node_report_num = 0
	while node_num != node_report_num:
		s.listen(5)
		sock, addr = s.accept()
		node_id = int(tr.get_file(sock, "tmp.txt"))
		os.rename("tmp.txt", "report_" + str(node_id) + ".txt")
		print "get report from node " + str(node_id)
		node_report_num = node_report_num + 1
	f = open("result.txt", 'w')
	for key in node_list:
		for line in fileinput.input("report_" + str(key) + ".txt"):
			nd, pr = line.split(' ')
			f.write(str(nd)+' '+str(pr))
			ele_list[nd] = pr
	f.close()
	print "next round"
	for key in node_list:
		f = open("update_"+str(key)+".txt", 'w')
		for ele in node_adj[key]:
			f.write(str(ele)+' '+str(ele_list[ele]))
		f.close()
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((node_list[key][0], node_list[key][1]))
		tr.send_file(sock, "update_"+str(key)+".txt", key)
		print "send update file to node "+str(key)	


s.close()