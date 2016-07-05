import fileinput
# return dict for id => (host, port)
def divide_graph(filename, nodenum):
	cnt = 0
	from_to_dict = {}
	for line in fileinput.input(filename):
		cnt = cnt + 1
		if cnt >= 5:
			src, dst = line.strip(' \n\r').split('\t')
			if not from_to_dict.has_key(src):
				from_to_dict[src] = {}
			from_to_dict[src][dst] = 1
	counter = 0
	eles_num = len(from_to_dict)
	per_node = (eles_num - 1) / nodenum + 1
	f = open("master_1.txt", 'w')
	for ele in from_to_dict:
		counter = counter + 1
		f.write(ele+'\n')
		if (counter % per_node == 0) and (counter < eles_num):
			f.close()
			f = open("master_"+str(counter / per_node + 1)+".txt", 'w')
	f.close()

	print "divide graph"
	return {}
