import numpy as np

def get_samples(filename):
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

if __name__ == "__main__":
    for sample in get_samples('data/infections_daily.csv'):
        print sample