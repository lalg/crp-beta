# Universal Portfolio Analysis
# Beta Version

## Introduction
TBD

## Installation

These installation notes has been verified on MacOS, and should work
on Linux (Windows is unlikely). There are two major steps: 

1. Installing open source and [required tools](#Required Tools)
2. [Downloading Universal Portfolio Analysis libraries](#Download Analysis Library)
	
Analysis is then done using 
[command line commands](#Portfolio Analysis)
in the shell.

### Required Tools
The analysis requires git, Python3, Java17, and Spark. This is a
beta-version and the installation and usage is somewhat complex, but
will be simplified in the future. Homebrew is used to manage part of
the installation.

#### git
   Git on the Mac is installed via Xcode. Saying `git --version` for
   the first time will prompt to install via Xcode.



**Brew**
The remaining
tools are easy to download and maintain using _brew_. If brew is not
present, then in the HOME directory, install using (see 
[Brew Installation](https://docs.brew.sh/Installation#untar-anywhere-unsupported)):

```shell
mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew
```
This creates a directory `homebrew` where everything is installed. The
end of the installation will print something similar to: 

```console
# Add Homebrew to your PATH in ~/.zprofile:
echo 'eval "$(<path>/homebrew/bin/brew shellenv)"' >> ~/.zprofile
```

Instead it is better to add to the end of the `.zshenv` file.
```console
eval $(/usr/local/bin/brew shellenv)
```

**Apache spark**
Download and install openjdk-17 and apache-spark using using: 
```shell
brew install openjdk@17
brew install apache-spark
```

Executing `spark-shell` in a new shell should produce something like:

```console
% spark-shell
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
24/03/27 10:45:28 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Spark context Web UI available at http://lals-mbp:4040
Spark context available as 'sc' (master = local[*], app id = local-1711550728899).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.5.1
      /_/
         
Using Scala version 2.12.18 (OpenJDK 64-Bit Server VM, Java 17.0.9)
Type in expressions to have them evaluated.
Type :help for more information.

scala> 
```
**Python**
The python environment is vast with its own
toolset to manages packages. Best to install python3.12 from the 
[official site](https://www.python.org/downloads/macos/) and use
its `pip3` to install the required packages:
```shell
pip3 install numpy
pip3 install matplotlib
pip3 install pandas
pip3 install yfinance
pip3 install pyarrow
```

When properly configured the following should succeed in the python3
shell: 
```
import numpy
import pandas
import matplotlib
import yfinance
```

### Download Analysis Library
Executing the following command will download the analysis library from
_github_, and create a directory `crp-beta`:
```shell
git clone https://github.com/lalg/crp-beta.git
```

## Portfolio Analysis
All portfolio analysis is performed at the shell command line
level. Executing the following in the `crp-beta` directory will
perform analysis of a portfolio consisting of AAPL, AMZN, MSFT, AMAT,
and GOOG.

```shell
code/bin/coversAnalysis --env prod --portfolio-name mag5 --training-rate 1.5 --comma-sep-sec "AAPL,MSFT,AMZN,GOOG,AMAT"
```
The command does the following:
1. Downloads price data from 2013 to the end of 2023 if it does not
   exist. The data is stored as a spark table in the `crp-beta`
   project.
   
2. Peforms wealth analysis of a universal portfolio, an
   equal-weighted reblanced portfolio, and the performance of the
   market as given by the S&P500.
   
3. Subsequent versions will compare a buy-and-hold performance.

4. Finally the various computed wealths and the weights for the
   portfolio are graphically displayed.
   
   
## TODO
To be done is an explanation of the training rate parameter, and
interpretation of analysis. 
