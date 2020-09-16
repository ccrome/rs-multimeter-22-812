import matplotlib.pyplot as plt
import argparse
import json
import numpy as np
import time
from datetime import datetime
from time import mktime

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("LOGFILE", help="Name of logfile to plot.  The logfile produced from rs22812.py")
    args = p.parse_args()
    return args

args = get_args()
f=open(args.LOGFILE)
v = []
times = []
try:
    while True:
        l = f.readline()
        j = json.loads(l)
        v.append(j["value"])
        t = j["time"]
        t = time.strptime(t, "%Y-%m-%d-%H:%M:%S")
        dt = datetime.fromtimestamp(mktime(t))
        times.append(dt)
except json.decoder.JSONDecodeError:
    pass

times = np.array(times, dtype=np.datetime64)
times = times-times[0]
times = np.array([t.item().total_seconds() for t in times])
values = np.array(v)
for t, v in zip(times, values):
    print(f'{t}, {v}')
plt.plot(times, values)
plt.show()
