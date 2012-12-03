import sys
import math 
import numpy as np



rainbow=['#2E0854', '#3A074E', '#470648', '#540643', '#61053D', '#6E0538', '#7A0432', '#87042C', '#940327', '#A10321', '#AE021C', '#BA0216', '#C70110', '#D4010B', '#E10005', '#EE0000']
rainbow=rainbow[::-1]


def graph_matrix(m):
	out = open('graph.gv', 'w')
	out.write("graph \"G\" {\nratio=1\n")
	
	s = m.shape[0]
	s = s/2
	for i in range(s):
		
		out.write("%d [pos=\"%d,%d!\"	];\n" % (i,i,i))
	out.write('\n')
	for i in range(s):	
		for j in range(s + i, s * 2):
			if i != j:
				magnitude = m[i][j]
				print magnitude
				if magnitude < 0:
					pass
				else:
					magnitude = min(magnitude * 8, 15)
					magnitude = int(round(magnitude))
					color=""
					for k in range(magnitude/4):
						color +=  rainbow[magnitude-1] + ':'
					color=color[:-1]
					j = j - s
					out.write("%d -- %d [color=\"%s\"];\n" %(i, j, color))
	out.write('}')


def graph_netinf(fname):
	print 'working'
	f = open(fname, 'r')
	out = open('netinf.gv', 'w')
	out.write('graph G {\n')
	writing = False
	rem = 200
	for line in f:
		if writing:
			line = [float(i) for i in line.split(',')]
			line[2] = int(round(line[2] + .49))
			if line[2]>6:
				line[2]=6
			color=""
			for i in range(line[2]):
				color +=  rainbow[line[2]-1] + ':'
			color=color[:-1]
			out.write("%d -- %d [color=\"%s\"];\n" %(line[0], line[1], color))
			rem = rem - 1
			if rem == 0:
				break
		elif len(line) < 3:
			writing= True
	out.close
	out.write('}\n')

if __name__=="__main__":
	if sys.argv[1] == 'netinf':
		graph_netinf(sys.argv[2])
	else:
		graph_matrix(open(sys.argv[2])["graph"])


	if sys.argv[1] == 'test':
		m = np.random.rand(40,40)
		pretty_graph.graph_matrix(m)



