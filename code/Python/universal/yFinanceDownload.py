# import data from yahoo finance 

#
# yFinanceDownload
#        ([--day date]   |
#         [--month date] |
#         [--year date]) |
#         [--startDate date --endDate date] symbols+
#  Examples
#     python3 yFinanceDownload.py --day 2022-09-01 EURUSD    
#

#
# TODO
#    1. parameter to select dev/prod for temp path
#

import sys
import getopt
from datetime import  datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import yfinance as yf
from env import Env

class YFinanceDownload :
    def __init__(self, sd, ed, holidays, backfill, env, *symbols) :
        self.startDate = sd
        self.endDate = ed
        self.holidays = holidays
        self.backfill = backfill
        self.envName = env
        self.symbols = symbols
        print(sd, ed)

    def universalEnv(self) :
        if self.envName in ("dev", "prod") : return Env(self.envName)
        else :
          raise Exception(f"{self.envName} -- envName not recognized")

    # approx size of data
    def sanityCheck(self, pDf) :
        days = np.busday_count(self.startDate, self.endDate)
        print("|df|={} |days|={}".format(len(pDf), days))
        
    def download(self) :
        syms = self.symbols[0].replace(" ", "").split(",")
        if len(syms) == 0 :
            raise Exception("yFinanceDownload: [warn] - no symbols found")

        elif len(syms) == 1 :
            return self.downloadSingle(self.symbols[0])
        
        else :
            return self.downloadMultiple(syms)

    # return pandas data frame
    def downloadSingle(self, symbol) :
        print(f"[INFO] {symbol} -- download")
        pDf = yf.download(symbol, start=self.startDate, end=self.endDate)
        if (self.startDate == self.endDate) :
            print(f"[INFO] - {symbol} -- no data")
            cols = [
                "date", "symbol", "open", "high", "low", "close",
                "volume", "year"]
                    
            return pd.DataFrame(columns=cols)
        
        elif (pDf.empty) :
            print(f"[INFO] - {symbol} -- no data")
            return pDf

        else :
            pDf.reset_index(inplace=True)

            renamed = (
                pDf
                  .rename(
                    columns = {
                        "Ticker" : "symbol",
                        "Date" : "date",
                        "Open" : "open",
                        "High" : "high",
                        "Low" : "low",
                        "Adj Close" : "close",
                        "Volume" : "volume"})
                  .sort_index(axis=1)
                  .drop("Close", axis=1))

            symbolX = symbol.replace("=X", "")
            renamed["symbol"] = [symbolX for i in range(0, len(renamed))]
            renamed["year"] = renamed["date"].dt.year
            renamed["date"] = renamed["date"].dt.date
            self.sanityCheck(renamed)
            return renamed

    # with multiple
    # pDf.stack(level=1).rename_axis(['date', 'symbol']).reset_index(level=1)        
    def downloadMultiple(self, symbols) :
        dfs = [self.downloadSingle(sym) for sym in symbols]
        all = pd.concat(dfs, ignore_index=True)
        self.sanityCheck(all)
        return all

    def save(self, df) :
        tp = self.universalEnv().tempRoot()
        if (self.backfill) :
            print(f"{tp}/backfill --- write")
            df.to_parquet(f'{tp}/backfill' )
        else :
            print(f"{tp}/prediction -- write")            
            df.to_parquet(f'{tp}/prediction')
        
    def downloadAndSave(self) :
        self.save(self.download())

        
if __name__ == '__main__' :
    optlist, symbols = (
        getopt.getopt(
            sys.argv[1:],
            'd:m:y:h:b:s:e:v:',
            ["day=",
             "month=",
             "year=",
             "holidays=",
             "backfill=",
             "start=",
             "end=",
             "env"]))

    def getDate(date) :
        return datetime.strptime(date, "%Y-%m-%d").date()

    # WTF is holidays!?
    holidays = 4
    env = "dev"
    backfill = True
    
    for opt, arg in optlist :
        if opt in ("--day", "-d") :
            startDate = getDate(arg)
            endDate = startDate + relativedelta(days=1)

        elif opt in ("--month", "-m") :
            startDate = getDate(arg)
            endDate = startDate + relativedelta(months=1, day=1)

        elif opt in ("--year", "-y") :
            startDate = getDate(arg)
            endDate = startDate + relativedelta(years=1, month=1, day=1)

        elif opt in ("--holidays", "-h") :
            holidays = int(arg)

        elif opt in ("--backfill", "-b") :
            if arg in ("true", "True") :
                backfill = True
            elif arg in ("false", "False") :
                backfill = False
            else :
                print(f"[ERROR] {arg} --- bad backfill")
                sys.exit(1)

        elif opt in ("--start", "-s") :
            startDate = getDate(arg)
            
        elif opt in ("--end", "-e") :
            endDate = getDate(arg)

        elif opt in ("--env", "-v") :
            # should be one of dev or prod
            env = arg
            
        else :
            print("{} -- unrecognized".format(opt))
            sys.exit(1)

    yfd = YFinanceDownload(startDate, endDate, holidays, backfill, env,  *symbols)
    yfd.downloadAndSave()
    sys.exit(0)
          
    

        
#     
