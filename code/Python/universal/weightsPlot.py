import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import sys
from env import Env


def readFile(file, sortBy) :
    df = pd.read_csv(file)
    return df.sort_values(by = sortBy)

def plot(df, dt, ynames) :
    df[dt] = pd.to_datetime(df[dt])
    x = df[dt]
    ys = [(yname, df[yname]) for yname in ynames]
    fig, ax = plt.subplots()
    for (yname, y) in ys :
        ax.plot(x, y, '-', label=yname)

    ax.set_title("Portfolio Weights")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weights")

    dateForm = mdates.DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(dateForm)
    ax.legend()
    plt.gcf().autofmt_xdate()
    plt.show(block=False)
    plt.show()
    
        
# takes name of file
if __name__ == '__main__' :
    envName = sys.argv[1]
    filename = sys.argv[2]
    env = Env(envName)
    filePath = "%s/%s.csv" % (env.projectTempData(), filename)
    df = readFile(filePath, "date")
    if (len(sys.argv) > 3) : ynames = sys.argv[3:]
    else :
        ynames = list(df.columns)
        ynames.remove("date")
        print("\nynames = %s" % ynames)

    plot(df, "date", ynames)
    
