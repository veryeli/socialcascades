import fileinput
import datetime
import dateutil.parser
from urlparse import urlparse
import operator
import pickle
import numpy as np

def min_start():
    starts = []
    ends = []
    mindate = None
    maxdate = None
    mode = 'A'
    bleft = 0
    cleft = 0
    lines_read = 0
    for line in fileinput.input():
        if lines_read < 6 or line.strip() == "":
            lines_read += 1
            continue
        tokens = line.split('\t')
        # parse A records
        if mode == 'A':
            assert(tokens[0] != "")
            mode = 'B'
            bleft = int(tokens[0])
            if mindate is None:
                continue
            print "{0} --- {1}".format(mindate, maxdate)
            print line
            starts.append(mindate)
            ends.append(maxdate)
            mindate = None
            maxdate = None
        # parse B records
        elif mode == 'B':
            assert(tokens[0] == "")
            assert(tokens[1] != "")
            mode = 'C'
            cleft = int(tokens[2])
            bleft -= 1
        elif mode == 'C':
            assert(tokens[0] == "")
            assert(tokens[1] == "")
            cur = dateutil.parser.parse(tokens[2])
            if mindate is None:
                mindate = cur
                maxdate = cur
            elif cur < mindate:
                mindate = cur
            elif cur > maxdate:
                maxdate = cur
            cleft -= 1
            if cleft == 0:
                if bleft == 0:
                    mode = 'A'
                else:
                    mode = 'B'

def toptlds():
    blogfreqs = {}
    mediafreqs = {}
    mode = 'A'
    acount = 0
    bcount = 0
    ccount = 0
    bleft = 0
    cleft = 0
    lines_read = 0
    for line in fileinput.input():
        if lines_read < 6 or line.strip() == "":
            lines_read += 1
            continue
        tokens = line.split('\t')
        # parse A records
        if mode == 'A':
            assert(tokens[0] != "")
            mode = 'B'
            bleft = int(tokens[0])
            acount += 1
            print line
            print "Lengths: Media={0} Blogs={1}".format(len(mediafreqs), len(blogfreqs))
        # parse B records
        elif mode == 'B':
            assert(tokens[0] == "")
            assert(tokens[1] != "")
            mode = 'C'
            cleft = int(tokens[2])
            bleft -= 1
            bcount += 1
        elif mode == 'C':
            assert(tokens[0] == "")
            assert(tokens[1] == "")
            host = urlparse(tokens[5]).hostname
            if tokens[4] == 'B':
                freqs = blogfreqs
            else:
                freqs = mediafreqs
            if not host in freqs:
                freqs[host] = 0
            freqs[host] -= 1
            cleft -= 1
            if cleft == 0:
                if bleft == 0:
                    mode = 'A'
                else:
                    mode = 'B'
            ccount += 1
    print 'A: {0} B: {1} C: {2}'.format(acount, bcount, ccount)
    sorted_blogs = sorted(blogfreqs.iteritems(), key=operator.itemgetter(1))
    sorted_media = sorted(mediafreqs.iteritems(), key=operator.itemgetter(1))
    pickle.dump(sorted_blogs, open('data/blogs.txt', "wb"), 0)
    pickle.dump(sorted_media, open('data/media.txt', "wb"), 0)

def count_occurs(hosts):
    mode = 'A'
    bleft = 0
    cleft = 0
    lines_read = 0
    blog_occurs = 0
    media_occurs = 0
    both_occurs = 0
    occurred_blog = 0
    occurred_media = 0
    blog_threshold = 20
    media_threshold = 10
    accepted_clusters = []
    for line in fileinput.input():
        if lines_read < 6 or line.strip() == "":
            lines_read += 1
            continue
        tokens = line.split('\t')
        # parse A records
        if mode == 'A':
            assert(tokens[0] != "")
            mode = 'B'
            bleft = int(tokens[0])
            if occurred_media >= media_threshold:
                media_occurs += 1
            if occurred_blog >= blog_threshold :
                blog_occurs += 1
            if occurred_blog >= blog_threshold and occurred_media >= media_threshold:
                both_occurs += 1
                accepted_clusters.append(cluster_id)
            occurred_media = 0
            occurred_blog = 0
            cluster_id = tokens[3]
            print line
        # parse B records
        elif mode == 'B':
            assert(tokens[0] == "")
            assert(tokens[1] != "")
            mode = 'C'
            cleft = int(tokens[2])
            bleft -= 1
        elif mode == 'C':
            assert(tokens[0] == "")
            assert(tokens[1] == "")
            host = urlparse(tokens[5]).hostname
            if host in hosts:
                if tokens[4] == 'B':
                    occurred_blog += 1
                else:
                    occurred_media += 1
            cleft -= 1
            if cleft == 0:
                if bleft == 0:
                    mode = 'A'
                else:
                    mode = 'B'
    print 'Media: {0} Blog: {1} Both: {2}'.format(media_occurs, blog_occurs, both_occurs)
    pickle.dump(sorted(accepted_clusters), open('data/cluster_ids.txt', 'wb'), 0)

def create_slices(hosts, clusters, slicer):
    infections = []
    infection = []
    mode = 'A'
    bleft = 0
    cleft = 0
    lines_read = 0
    infection_count = 0
    valid_cluster = False
    f = open('data/infections_daily.csv', 'wb')
    for line in fileinput.input():
        if lines_read < 6 or line.strip() == "":
            lines_read += 1
            continue
        tokens = line.split('\t')
        # parse A records
        if mode == 'A':
            assert(tokens[0] != "")
            mode = 'B'
            bleft = int(tokens[0])
            if valid_cluster:
                for sample in infection:
                    f.write(','.join(sample) + '\n')
                f.write('\n')
                f.flush()
                infection = []
            cluster_id = tokens[3]
            valid_cluster = cluster_id in clusters
            if valid_cluster:
                #infections.append([])
                print line
        # parse B records
        elif mode == 'B':
            assert(tokens[0] == "")
            assert(tokens[1] != "")
            mode = 'C'
            cleft = int(tokens[2])
            bleft -= 1
        elif mode == 'C':
            assert(tokens[0] == "")
            assert(tokens[1] == "")
            if valid_cluster:
                host = urlparse(tokens[5]).hostname
                if host in hosts:
                    hostIdx = hosts[host]
                    date = dateutil.parser.parse(tokens[2])
                    idx = slicer(date)
                    #infection = infections[-1]
                    while idx >= len(infection):
                        #infection.append(np.zeros(len(hosts)))
                        infection.append(['0' for x in hosts])
                    infection[idx][hostIdx] = '1'
            cleft -= 1
            if cleft == 0:
                if bleft == 0:
                    mode = 'A'
                else:
                    mode = 'B'
    # if len(infections) > 0:
    #     pickle.dump(infections, open('data/infections{0}.data'.format(infection_count), 'wb'))

def hour_slices(date):
    diff = date - datetime.datetime(2008, 8, 1)
    hours = diff.total_seconds() / 3600
    return int(hours)

def day_slices(date):
    diff = date - datetime.datetime(2008, 8, 1)
    days = diff.total_seconds() / (3600 * 24)
    return int(days)

def firstn(n):
    count = 0
    for line in fileinput.input():
        print line
        count += 1
        if count == n:
            break

def parse(self, timestep):
    pass

if __name__ == "__main__":
    #print min_start()
    #toptlds()
    #firstn(100)
    hosts_list = pickle.load(open('data/media.txt', "rb"))[0:20] + pickle.load(open('data/blogs.txt', "rb"))[0:40]
    hosts = dict((host[0], i) for i,host in enumerate(hosts_list))
    clusters = pickle.load(open('data/cluster_ids.txt', 'rb'))
    pickle.dump(hosts, open('data/nodes.txt', 'wb'), 0)
    #count_occurs(hosts)
    create_slices(hosts, clusters, day_slices)

