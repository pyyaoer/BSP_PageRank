import os
import struct

def get_file(sock, filename):
	FILEINFO_SIZE = struct.calcsize('iI')
	fhead = sock.recv(FILEINFO_SIZE)
	node_id, restsize = struct.unpack('iI', fhead)
	fp = open(filename,'wb')
	while 1:
		if restsize > 1024:
			filedata = sock.recv(1024)
		else:
			filedata = sock.recv(restsize)
			fp.write(filedata)
			break
		if not filedata:
			break
		fp.write(filedata)
		restsize = restsize - len(filedata)
		if restsize <= 0:
			break
	fp.close()
	return node_id

def send_file(sock, filename, node_id):
	FILEINFO_SIZE = struct.calcsize('iI')
	fhead = struct.pack('iI', node_id, os.stat(filename).st_size)
	sock.send(fhead)
	try:
		fp = open(filename, 'rb')
		while True:
			filedata = fp.read(1024)
			if not filedata:
				break
			sock.send(filedata)
		fp.close()
	except Exception, e:
		raise
