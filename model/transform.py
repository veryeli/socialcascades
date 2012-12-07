from get_samples import get_samples
import sys

def transform_to_netinf(fname):
	f = open(fname.replace('.csv','.netinf'), 'wb')
	for sample in get_samples(fname):
		numvars= sample.shape[1]

	for i in range(numvars):
		f.write("%s,%s\n" %(i,i))

	total = 0

	for sample in get_samples(fname):
		numvars= sample.shape[1]
		netinf = {}
		print total
		for i in range(sample.shape[0]):
			for j in range(sample.shape[1]):
				if sample[i,j] == 1:
					if j not in netinf:
						netinf[j] = i
		f.write('\n')
		for item in netinf.keys():
			f.write('%s,%s;' % (item, netinf[item]))
		total += 1

if __name__ == "__main__":
	prefix = sys.argv[1]
	splits = int(sys.argv[2])
	for i in range(splits):
		print "Converting {0}".format(i)
		transform_to_netinf(prefix + "_test" + str(i) + ".csv")
		transform_to_netinf(prefix + "_train" + str(i) + ".csv")
