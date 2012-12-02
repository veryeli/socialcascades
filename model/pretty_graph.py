import sys
import math 
import numpy as np



rainbow=['#D92727', '#D72E32', '#D6363E', '#D43E4A', '#D34656', '#D14E62', '#D0566E', '#CE5E7A', '#CD6686', '#CC6D92', '#CA759E', '#C97DAA', '#C785B6', '#C68DC2', '#C495CE', '#C39DDA', '#C2A5E6']
rainbow=rainbow[::-1]


def graph_matrix(m):
	out = open('graph.gv', 'w')
	out.write("graph G {\n")
	#out.write("size=[10,10]\n")
	s = m.shape[0]
	print s
	for i in range(s):
		for j in range(s):
			if i != j:
				if m[i,j]>=.9:
					magnitude = int(((round(m[i,j] * 10) - 9)* 16))
					color=""
					for k in range(magnitude/2):
						color +=  rainbow[magnitude-1] + ':'
					color=color[:-1]
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