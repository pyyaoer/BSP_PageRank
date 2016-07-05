import fileinput
# return dict for id => (host, port)
def divide_graph(filename, nodenum):
	cnt = 0
	from_to_dict = {}
	to_from_dict = {}
	node_dict = {}
	for line in fileinput.input(filename):
		cnt = cnt + 1
		if cnt >= 5:
			src, dst = line.strip(' \n\r').split('\t')
			if not from_to_dict.has_key(src):
				from_to_dict[src] = {}
			from_to_dict[src][dst] = None
			if not to_from_dict.has_key(dst):
				to_from_dict[dst] = {}
			to_from_dict[dst][src] = None
	counter = 0
	node_cnt = 1
	eles_num = len(from_to_dict)
	per_node = (eles_num - 1) / nodenum + 1
	f = open("task_"+str(node_cnt)+".txt", 'w')
	node_dict[node_cnt] = {}
	for ele in from_to_dict:
		counter = counter + 1
		node_dict[node_cnt][ele] = None
		f.write(ele)
		for key in from_to_dict[ele]:
			f.write(' ' + str(key))
		f.write('\n')
		if (counter % per_node == 0) and (counter < eles_num):
			f.close()
			node_cnt = node_cnt + 1
			node_dict[node_cnt] = {}
			f = open("task_"+str(node_cnt)+".txt", 'w')
	f.close()

	print "divide graph"
	return {}
