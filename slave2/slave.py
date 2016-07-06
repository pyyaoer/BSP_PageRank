import os
import sys
import socket
import bsp_tr as tr

Generation = 0
KeepRuning = True
Map = {}
Rank = {}
OutRate = {}
MyNode = {}
delta = 0.001
node_id = 0

# wait for master to sync
def sync(sock):
	global Generation
	s.listen(5)
	sock, addr = s.accept()
	tr.get_file(sock,"Master_Data"+str(Generation)+".txt")
	
	f = open("Master_Data"+str(Generation)+".txt", "r")
	while True:
		line = f.readline()
		a = line.strip("\n").split(" ")
		if len(a) < 2:
			break
		a1 = int(a[0])
		a2 = float(a[1])
		Rank[a1] = a2

	Generation = Generation + 1
	print "Waiting for Master to Syncornize"
	return True

# calculate rank value
def calc():
	global Map
	global Rank
	global delta
	global KeepRuning
	global OutRate
	anyChange = False
	oldRank = Rank.copy()
	#print oldRank
	for key in Rank:
		Rank[key] = 0
	for key1 in Map:
		neighbor = Map[key1]
		for key2 in neighbor:
			#print oldRank[int(key2)]
			Rank[key1] = Rank[key1] + oldRank[int(key2)] / (OutRate[int(key2)] + 0.0)
		Rank[key1] = Rank[key1] + 0.15

	for key in Map:
		#print oldRank[key] , Rank[key]
		if abs(oldRank[key] - Rank[key]) > delta:
			anyChange = True
			break

	if not anyChange:
		KeepRuning = False
	#print Rank
	print "Page Ranking"
	return

# send the result to Master
def report(socket,FileName,node_id):
	tr.send_file(socket,FileName,node_id)
	print "Sending Rank Data to Master"
	return

# save the calc data
def save(Generation):
	global Map
	global Rank
	f = open("Result-"+str(Generation)+".txt","w")
	for key in Rank:
		if Map.has_key(key):
			f.write(str(key)+" "+str(Rank[key])+"\n")
	f.close()
	print "Saving Result" , Generation
	return

# load the init data
def load(FileName):
	global Map
	global Rank
	global OutRate
	global MyNode
	f = open(FileName,"r")
	line = f.readline()
	line = line.strip("\n")
	count  = int(line)

	while count > 0:
		line = f.readline()
		a = line.strip("\n").split(" ")
		#print a
		a1 = int(a[0])
		a2 = int(a[2])
		if not OutRate.has_key(a1):
			OutRate[a1] = 0
		if not Rank.has_key(a1):
			Rank[a1] = 0
		OutRate[a1] = a2
		count = count - 1
		
	while True:
		line = f.readline()
		if not line:
			break
		a = line.strip("\n").split(" ")
		a0 = int(a[0])
		#print a0
		b = a[1:]
		#print b
		MyNode[a0] = 0
		Map[a0] = []
		Map[a0] = b
		for key in b:
				if not Rank.has_key(key):
					Rank[key] = 0
	f.close()
	#print Map
	print "Loadding Result" , Generation
	return

# continue for a crash
def reload(Generation):
	print "Restoring Data From" , Generation
	return

def final_report(sock):
	tr.send_file(sock,"",-node_id)
	return

port = int(sys.argv[1])
host = 'localhost'
master_port = 9000
master_host = "127.0.0.1"

DataName = "MasterInitData.txt"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
# get partition infomation from master
sock, addr = s.accept()
node_id = int(tr.get_file(sock,"tmp.txt"))
if node_id <= 0:
	node_id = -node_id
	f = open("tmp.txt")
	Generation = int(f.readline());
else:
	os.rename("tmp.txt", DataName)

load(DataName)
while KeepRuning:
	calc()
	save(Generation)
	send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	send_sock.connect((master_host, master_port))
	report(send_sock,"Result-"+str(Generation)+".txt",node_id)
	sync(s)

send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_sock.connect((master_host, master_port))
final_report(send_sock)
s.close()
send_sock.close()