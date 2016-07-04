import bsp_lc as lc
import bsp_cm as cm
import bsp_bs as bs

def receive_task():
	pass

receive_task()
while True:
	lc.local_compute()
	cm.send_messages()
	if bs.barrier_sync():
		break