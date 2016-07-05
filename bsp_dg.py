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
	eles_num = len(to_from_dict)
	per_node = (eles_num - 1) / nodenum + 1
	f = open("task_"+str(node_cnt)+".txt", 'w')
	node_dict = {}
	for ele in to_from_dict:
		counter = counter + 1
		node_dict[ele] = node_cnt
		f.write(ele)
		for key in to_from_dict[ele]:
			f.write(' ' + str(key))
		f.write('\n')
		if (counter % per_node == 0) and (counter < eles_num):
			f.close()
			node_cnt = node_cnt + 1
			f = open("task_"+str(node_cnt)+".txt", 'w')

	node_map = {}
	for ele in from_to_dict:
		if not node_dict.has_key(ele):
			node_dict[ele] = nodenum
			f.write(str(ele) + '\n')
		node_src = node_dict[ele]
		if not node_map.has_key(node_src):
			node_map[node_src] = {}
		for key in from_to_dict[ele]:
			node_map[node_src][node_dict[key]] = None
	f.close()

	f = open("nodemap.txt", 'w')
	for ele in node_map:
		f.write(str(ele))
		for key in node_map[ele]:
			f.write(' ' + str(key))
		f.write('\n')
	f.close()

	print "divide graph"
	return {}
