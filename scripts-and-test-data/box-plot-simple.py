#!/usr/bin/env python

import sys
import pylab
import numpy

summary_file = sys.argv[1]
param_num = int(sys.argv[2])
out_file = sys.argv[3]

to_plot = [[] for i in xrange(param_num)]
with open(summary_file, 'r') as f:
    for line in f:
        entries = line.split()[-param_num:]
        for i in xrange(param_num):
            to_plot[i].append(float(entries[i]))

pylab.figure(figsize=(3*param_num, 2.5))
for i in xrange(param_num):
    pylab.subplot(1, param_num, i + 1)
    pylab.boxplot(to_plot[i])
    pylab.xticks([1], '')
    pylab.xlabel('{0:.6f}'.format(numpy.median(numpy.array(to_plot[i]))))

pylab.tight_layout()
pylab.savefig(out_file)

