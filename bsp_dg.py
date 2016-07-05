import fileinput
def divide_graph(filename, nodenum):
	cnt = 0
	from_to_dict = {}
	to_from_dict = {}
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

	element_degree = {}
	for ele in from_to_dict:
		element_degree[ele] = [0, len(from_to_dict[ele])]
	for ele in to_from_dict:
		if not element_degree.has_key(ele):
			element_degree[ele] = [len(to_from_dict[ele]), 0]
		else:
			element_degree[ele][0] = len(to_from_dict[ele])

	for i in range(1, nodenum+1):
		f = open("task_"+str(i)+".txt", 'w')
		f.write(str(len(element_degree)) + '\n')
		for ele in element_degree:
			tf = element_degree[ele]
			f.write(str(ele) + ' ' + str(tf[0]) + ' ' + str(tf[1]) + '\n')
		f.close()

	counter = 0
	node_cnt = 1
	eles_num = len(to_from_dict)
	per_node = (eles_num - 1) / nodenum + 1
	f = open("task_"+str(node_cnt)+".txt", 'aw')
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
			f = open("task_"+str(node_cnt)+".txt", 'aw')
	for ele in from_to_dict:
		if not node_dict.has_key(ele):
			node_dict[ele] = nodenum
			f.write(str(ele) + '\n')
	f.close()

	node_adj = {}
	for ele in to_from_dict:
		nd = node_dict[ele]
		if not node_adj.has_key(nd):
			node_adj[nd] = {}
		for key in to_from_dict[ele]:
			node_adj[nd][key] = None

	return node_adj

