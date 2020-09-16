import argparse
import pandas
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("FILE", nargs='+', help="Files of comma separated data to plot")
    p.add_argument("--xoffsets", nargs='+', help="Add xoffsets in time for each plot.  must be same length as FILE if used.", type=float)
    p.add_argument("-w", "--filter-window", type=int, help="smooth the plot with a filter of this many samples.", nargs='+', default=None)
    args = p.parse_args()
    if args.xoffsets is not None:
        assert(len(args.xoffsets) == len(args.FILE))
    if args.filter_window is not None:
        assert(len(args.filter_window) == len(args.FILE))
    return args

args = get_args()
for i, fn in enumerate(args.FILE):
    xoffset = 0
    filter_len = 1.1
    if args.xoffsets is not None:
        xoffset = args.xoffsets[i]
    if args.filter_window is not None:
        filter_len = args.filter_window[i]
    b, a = sig.butter(N=2, Wn=(1.0/filter_len))
    df = pandas.read_csv(fn)
    x = df.iloc[:,0].to_numpy()
    y = df.iloc[:,1]

    x = x + xoffset

    x2 = x
    #y2 = sig.lfilter(np.ones(filter_len)/filter_len, [1], y)
    y2 = sig.lfilter(b, a, y)


    plt.plot(x, y, label=fn)
    plt.plot(x2, y2, label=fn)
plt.grid()
plt.legend(loc="upper left")
plt.show()
