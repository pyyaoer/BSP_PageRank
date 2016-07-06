import os
import socket
import fileinput
import bsp_dg as dg
import bsp_tr as tr

generation = 0
ele_list = {}
finish_list = {}

node_list = {}
node_list[1] = ("localhost", 8001)
node_list[2] = ("localhost", 8002)

port = 9000
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
#s.listen(5)

if os.path.isfile("metadata.txt"):
	f = open("metadata.txt")
	try:
		generation = int(f.readline())
	except Exception, e:
		generation = 0
	f.close()
if os.path.isfile("tmp_meta.txt"):
	f = open("tmp_meta.txt")
	tmp_generation = generation
	try:
		generation = int(f.readline())
	except Exception, e:
		generation = tmp_generation
	f.close()

# divide the graph and generates the partition txt
node_num = len(node_list)
node_adj = dg.divide_graph("wiki-Vote.txt", node_num, generation)

# send partition infomation to slaves
for key in node_list:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((node_list[key][0], node_list[key][1]))
	if generation != 0:
		tr.send_file_master(sock, "task_"+str(key)+".txt", -key)
		print "recover node "+str(key)+" from generation "+str(generation)
	else:
		tr.send_file_master(sock, "task_"+str(key)+".txt", key)
		print "send task file to node "+str(key)

while node_num != 0:
	node_report_num = 0
	tmp_node_num = node_num
	while node_num != node_report_num:
		node_report_num = node_report_num + 1
		s.listen(5)
		sock, addr = s.accept()
		node_id = int(tr.get_file_master(sock, "tmp.txt"))
		if node_id <= 0:
			tmp_node_num = tmp_node_num - 1
			finish_list[-node_id] = None
			continue
		os.rename("tmp.txt", "report_" + str(node_id) + ".txt")
		print "get report from node " + str(node_id)
	node_num = tmp_node_num
	f = open("result.txt", 'w')
	for key in node_list:
		for line in fileinput.input("report_" + str(key) + ".txt"):
			nd, pr = line.split(' ')
			f.write(str(nd)+' '+str(pr))
			ele_list[nd] = pr
	f.close()
	# checkpoint
	f = open("tmp_meta.txt", 'w')
	generation = generation + 1
	f.write(str(generation))
	f.close
	for key in node_list:
		if (finish_list.has_key(key)):
			continue
		f = open("update_"+str(key)+".txt", 'w')
		for ele in node_adj[key]:
			f.write(str(ele)+' '+str(ele_list[ele]))
		f.close()
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((node_list[key][0], node_list[key][1]))
		tr.send_file_master(sock, "update_"+str(key)+".txt", key)
		print "send update file to node "+str(key)	

s.close()