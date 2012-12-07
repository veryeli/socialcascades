import numpy as np
import sys
def get_samples(filename):
    with open(filename) as f:
        rows = []
        for line in f:
            if len(line.strip()) == 0:
                arr = np.matrix(rows)
                rows = []
                yield arr
            else:
                tokens = line.split(',')
                row = [int(x) for x in tokens]
                rows.append(row)

def get_samples_netinf(filename):
    with open(filename) as f:
        rows = []
        prev = []
        for line in f:
            if len(line.strip()) == 0:
                arr = np.matrix(rows)
                rows = []
                yield arr
            else:
                tokens = line.split(',')
                row = [int(x) for x in tokens]
                if len(prev) > 0:
                    for i,n in enumerate(prev):
                        if prev[i] == 1:
                            row[i] = 1
                rows.append(row)

def get_train_samples(filename, steps):
    with open(filename) as f:
        rows = []
        for line in f:
            if len(line.strip()) == 0:
                arr = np.array(rows)
                rows = []
                yield arr
            else:
                tokens = line.split(',')
                row = [int(x) for x in tokens]
                rows.append(row)
                if len(rows) >= steps:
                    yield np.array(rows)
                    rows = rows[1:]



if __name__ == "__main__":
    for sample in get_samples('data/infections_daily.csv'):
        print sample