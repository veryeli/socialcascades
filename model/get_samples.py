import fileinput
import numpy as np
import sys
def get_samples(filename):
    with open(filename) as f:
        rows = []
        i=0
        for line in f:
            if len(line.strip()) == 0:
                i += 1
                arr = np.array(rows)
                rows = []
                yield arr
                if i == 5:
                    return
            else:
                tokens = line.split(',')
                row = [int(x) for x in tokens]
                rows.append(row)

if __name__ == "__main__":
    for sample in get_samples('data/infections_daily.csv'):
        print sample