#!/usr/bin/python
# -*- coding: utf-8 -*-
import matplotlib
import json
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import os, sys,ocrolib,argparse
from pylab import plot,title,show



parser = argparse.ArgumentParser(description = "Compute errors from saved models from ocropus-rtrain")
# input files
parser.add_argument("files",nargs="+",
help="input files; glob and @ expansion performed")


args = parser.parse_args()

files = args.files

str1=files[0]
fname_out=str1[0:str1.rfind('-')]+'-error'
f = open(fname_out+'.txt', 'w')
err = []
count = 0
m_name = []
for model in files:
    network = ocrolib.load_object(model)
    err.append(network.error)
    m_name.append(model)
    count += 1

data = {}
data['minimum'] = {
    'name': m_name[err.index(min(err))],
    'error': min(list(err))
}
data['last'] = {
    'name': m_name[-1],
    'error': list(err)[-1]
}

json.dump(data, f)

f.close()

fig = plt.figure()
plt.plot(err)
plt.title("%.2f,%s,%d"%(min(err),m_name[err.index(min(err))],len(files)))
plt.xlim([0,150])
plt.ylim([0,100])
fig.savefig(fname_out+'.png')
