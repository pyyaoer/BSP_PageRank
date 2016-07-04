import os
import struct

def get_file(sock, filename):
	FILEINFO_SIZE = struct.calcsize('128sI')
	while 1:
		try:
			fhead = sock.recv(FILEINFO_SIZE)
			filename_, filesize = struct.unpack('128sI', fhead)
			fp = open(filename,'wb')
			restsize = filesize
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
				restsize = testsize - len(filedata)
				if restsize <= 0:
					break
			fp.close()
		except:
			break

def send_file(sock, filename):
	FILEINFO_SIZE = struct.calcsize('128sI')
	fhead = struct.pack('128sI', filename, os.stat(filename).st_size)
	sock.send(fhead)
	try:
		fp = open(filename, 'rb')
		while True:
			print 'hehe'
			filedata = fp.read(1024)
			if not filedata:
				break
			sock.send(filedata)
		fp.close()
	except Exception, e:
		raise
