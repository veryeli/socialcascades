from get_samples import get_samples


def transform_to_netinf(fname):
	f = open(fname+'.netinf', 'w')
	for t in get_samples(samples):
		netinf = {}
		line = example[t]
		for i in len(line):
			if line[i] == 1:
				if i not in netinf.keys():
					netinf[i] = t
	entries = []
	for item in netinf.keys():
		entries.append(item, entries[item])