import sys
import socket
import bsp_lc as lc
import bsp_cm as cm
import bsp_bs as bs
import bsp_tr as tr

def receive_task():
	pass

port = int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

receive_task()
while True:
	lc.local_compute()
	cm.send_messages()
	if bs.barrier_sync():
		break

s.close()