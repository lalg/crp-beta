import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import sys
from env import Env

def readFile(file, sortBy = "date") :
    df = pd.read_csv(file)
    return df.sort_values(by = sortBy)

def plot(ax, df, dt, ynames) :
    df[dt] = pd.to_datetime(df[dt])
    x = df[dt]
    ys = [(yname, df[yname]) for yname in ynames]
    for (yname, y) in ys :
       ax.plot(x, y, '-', label=yname)
       
    ax.set_title("Portfolios Wealth")
    ax.set_xlabel("Date")
    ax.set_ylabel("Wealth")
    
    dateForm = mdates.DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(dateForm)
    ax.legend()

def driver(envName, portfolioName) :
    env = Env(envName)

    weightsFile = "%s/%s-wts.csv" % (env.projectTempData(), portfolioName)
    wealthFile = "%s/%s-wlt.csv" % (env.projectTempData(), portfolioName)
    weightsDf = readFile(weightsFile, "date")
    wealthDf = readFile(wealthFile, "date")

    fig, axs = plt.subplots(2, figsize=(10,7))
    fig.suptitle("Universal Portfolio Analysis")
    wlt_ynames = list(wealthDf.columns)
    wlt_ynames.remove("date")
    wts_ynames = list(weightsDf.columns)
    wts_ynames.remove("date")
    plot(axs[0], wealthDf, "date", wlt_ynames)
    plot(axs[1], weightsDf, "date", wts_ynames)
    plt.show()

if __name__ == '__main__' :
    envName = sys.argv[1]
    portfolioName = sys.argv[2]
    driver(envName, portfolioName)

    
