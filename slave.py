import sys
import socket
import bsp_lc as lc
import bsp_cm as cm
import bsp_bs as bs
import bsp_tr as tr

Generation = 0
KeepRuning = True
Map = {}
Rank = {}
OutRate = {}
delta = 0
# wait for master to sync
def sync(sock):
	global Generation
	#tr.get_file(sock,"Master_Data"+Generation)
	Generation = Generation + 1
	print "Waiting for Master to Syncornize"
	return True

# calculate rank value
def calc():
	global Map
	global Rank
	global delta
	global KeepRuning
	anyChange = False
	oldRank = Rank.copy()
	for key in Rank:
		Rank[key] = 0
	for key1 in Map:
		neighbor = Map[key1]
		for key2 in neighbor:
			Rank[key1] = Rank[key1] + oldRank[key2] / (OutRate[key2]+ 0.0)
		Rank[key1] = Rank[key1] + 0.15

	for key in Rank:
		#print oldRank[key] , Rank[key]
		if abs(oldRank[key] - Rank[key]) > delta:
			anyChange = True
			break

	if not anyChange:
		KeepRuning = False
	print Rank
	print "Page Ranking"
	return

# send the result to Master
def report():
	print "Sending Rank Data to Master"
	return

# save the calc data
def save(Generation):
	global Rank
	f.open("Result"+Generation,w)
	for key in Rank
		f.write(key," ",Rank[key])
	
	print "Saving Result" , Generation
	return

# load the init data
def load(FileName):
	global Map
	global Rank
	f = open(FileName,"r")
	while True:
		line = f.readline()
		if not line:
			break
		a = line.strip("\n").split(" ")
		a0 = int(a[0])
		print a0
		b = a[1:]
		print b
		if not Rank.has_key(a0):
			Rank[a0] = 0
		Map[a0] = []
		Map[a0] = b
		for key in b:
				if not Rank.has_key(key):
					Rank[key] = 0
	f.close
	#print Map
	print "Loadding Result" , Generation
	return

# continue for a crash
def reload(Generation):
	print "Restoring Data From" , Generation
	return

def build_adjnodes():
	return []

port = int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
master_port = 9000
master_host = "127.0.0.1"

# whether the adjacent node has sent the message
adjacent_nodes = {}
DataName = "MasterInitData.txt"
global Map

# get partition infomation from master
#while True:
#	sock, addr = s.accept()
#	node_id = int(tr.get_file(sock,DataName))
#	if (node_id == 0):
#		n_list = build_adjnodes()
#		for key in n_list:
#			if not adjacent_nodes.has_key(key):
#				adjacent_nodes[key] = False
#		break
#	adjacent_nodes[node_id] = True

load(DataName)
while KeepRuning:
	calc()
	save(Generation)
	report()
	sync(s)


s.close()