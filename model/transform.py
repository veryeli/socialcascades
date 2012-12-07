from get_samples import get_samples


def transform_to_netinf(fname):
	f = open(fname+'.netinf', 'w')
	for sample in get_samples(fname):
		numvars= sample.shape[1]

	for i in range(numvars):
		f.write("%s,%s\n" %(i,i))
		
	for sample in get_samples(fname):
		numvars= sample.shape[1]
		netinf = {}
		for i in range(sample.shape[0]):
			for j in range(sample.shape[1]):
				if sample[i][j] == 1:
					if i not in netinf.keys():
						netinf[j] = i 

		f.write('\n')
		for item in netinf.keys():
			f.write('%s,%s;' % (item, netinf[item]))