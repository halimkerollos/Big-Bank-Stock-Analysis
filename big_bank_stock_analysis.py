# Finance Data Project
#
# Disclaimer: This project is just meant to practice visualization
# and pandas skills, it is not meant to be a robust financial analysis
# or be taken as financial advice.
# ____
# We'll focus on bank stocks and see how they progressed throughout the
# 2008 financial crsis.

import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import cufflinks as cf
from pandas_datareader import data, wb
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# get_ipython().run_line_magic('matplotlib', 'inline')


# ## Data
#
# We need to get data using pandas datareader.
# We will get stock information for the following banks:
# * Bank of America
# * CitiGroup
# * Goldman Sachs
# * JPMorgan Chase
# * Morgan Stanley
# * Wells Fargo


BAC = data.DataReader("BAC", "stooq", "Jan 1 2006")
C = data.DataReader("C", "stooq", "Jan 1 2006")
GS = data.DataReader("GS", "stooq", "Jan 1 2006")
JPM = data.DataReader("JPM", "stooq", "Jan 1 2006")
MS = data.DataReader("MS", "stooq", "Jan 1 2006")
WFC = data.DataReader("WFC", "stooq", "Jan 1 2006")


# Create a list of the ticker symbols (as strings) in alphabetical order.
# Call this list: ticker


tickers = ["BAC", "C", "GS", "JPM", "MS", "WFC"]


# Use pd.concat to concatenate the bank dataframes together to a single data
# frame called bank_stocks. Set the keys argument equal to the tickers list.
# Also pay attention to what axis you concatenate on


bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC], keys=tickers, axis=1)
bank_stocks.tail()


# Set the column name levels


bank_stocks.columns.names = ["Bank Ticker", "Stock Info"]


# Check the head of the bank_stocks dataframe


bank_stocks.head()


# # EDA
#
# Let's explore the data a bit!
#
# What is the max Close price for each bank's stock throughout the time period


bank_stocks.xs(key="Close", axis=1, level="Stock Info").max()


# Create a new empty DataFrame called returns.
# This dataframe will contain the returns for each bank's stock.
# returns are typically defined by
#
# $$r_t = \frac{p_t - p_{t-1}}{p_{t-1}} = \frac{p_t}{p_{t-1}} - 1$$

# We can use pandas pct_change() method on the Close column to create
# a column representing this return value. Create a for loop that goes
# and for each Bank Stock Ticker creates this returns column and set's it
# as a column in the returns DataFrame


returns = pd.DataFrame()
for tick in tickers:
    returns[tick + " Return"] = bank_stocks[tick]["Close"].pct_change()


returns.tail()


# Create a pairplot using seaborn of the returns dataframe.
# What stock stands out to you? Can you figure out why
sns.set_theme(context="notebook", style="whitegrid", palette="viridis")
sns.pairplot(data=returns)


# I found that the data for Citibank did not match the course series pairplot
# and the explaination for this on the Q&A was that it was probably affected
# by a stock split between the course compilation and now. Solution:
# use the pickle file with the data that was provided with the course,
# frozen in time.
# Why this is unsatisfying to me: I don't understand, nor can I accept,
# how a stock split or any event for that matter would affect data from the
# past that was already recorded and I don't like the thought of past data
# being changed or manipulated.
# For now I will proceed with theassignment without
# worrying too much about why the data doesn't match,
# and finding extra correlations
# and visualizations that are of interest to me.

# Using this returns DataFrame, figure out on what dates each bank stock
# had the best and worst single day returns. You should notice that 4 of the
# banks share the same day for the worst drop, did anything significant happen
# that day


returns.idxmin()


returns.idxmax()


# You should have noticed that Citigroup's largest drop and biggest gain
# were very close to one another, did anythign significant happen in that
# time frame?

# Take a look at the standard deviation of the returns,
# which stock would you classify as the riskiest over the entire time period?
# Which would you classify as the riskiest for the year 2015

# Citibank does look like the most volatile of all the banks judging
# by it's std overall


returns.std()


returns.loc["2015-01-01":"2016-01-01"].std()


# Create a distplot using seaborn of the 2015 returns for Morgan Stanley
plt.figure(figsize=(12, 6))
sns.displot(
    returns.loc["2015-01-01":"2016-01-01"]["JPM Return"],
    kind="hist",
    kde=True,
    bins=70,
)


# Create a distplot using seaborn of the 2008 returns for CitiGroup
plt.figure(figsize=(10, 6))
sns.displot(
    data=returns.loc["2008-01-01":"2009-01-01"]["C Return"],
    kind="hist",
    kde=True,
    bins=70,
)


# A lot of this project will focus on visualizations.
sns.set_style("whitegrid")
get_ipython().run_line_magic("matplotlib", "inline")

# Optional Plotly Method Imports

cf.go_offline()
init_notebook_mode(connected=True)


# Create a line plot showing Close price for each bank
# for the entire index of time.

close = bank_stocks.xs(key="Close", axis=1, level="Stock Info")
close.iplot(kind="scatter", mode="lines+markers", size=0.5, width=0.5)


# The above is one I made with plotly and so it's interactive in that
# you can see the values you hover over with the curseer.
# But it takes a lot of computing power and makes everything lag,
# so I'm going to continue with seaborn.


plt.figure(figsize=(16, 6))
sns.lineplot(
    data=bank_stocks.xs(key="Close", axis=1, level="Stock Info"),
    markers=False,
)


bank_stocks.xs(key="Close", axis=1, level="Stock Info").iplot()


# ## Moving Averages
# Let's analyze the moving averages for these stocks in the year 2008.
# Plot the rolling 30 day average against the Close Price for
# Bank Of America's stock for the year 2008


plt.figure(figsize=(18, 6))
sns.lineplot(
    data=bank_stocks["BAC"].loc["2008-01-01":"2009-01-01"]["Close"].rolling(30).mean(),
    label="30 Day Avg",
)
sns.lineplot(
    data=bank_stocks["BAC"].loc["2008-01-01":"2009-01-01"]["Close"],
    label="BAC Close",
)


# Create a heatmap of the correlation between the stocks Close Price


sns.heatmap(
    bank_stocks.xs(key="Close", axis=1, level="Stock Info").corr(),
    cmap="magma",
    annot=True,
)


sns.clustermap(
    bank_stocks.xs(key="Close", axis=1, level="Stock Info").corr(),
    cmap="magma",
    annot=True,
)


# # Part 2
#

# Use .iplot(kind='candle) to create a candle plot of Bank of America's
# stock from Jan 1st 2015 to Jan 1st 2016


close_corr = bank_stocks.xs(key="Close", axis=1, level="Stock Info").corr()
close_corr.iplot(kind="heatmap", colorscale="rdylbu")


bank_stocks["BAC"].loc["2015-01-01":"2016-01-01"].iplot(kind="candle")


# Use .ta_plot(study='sma') to create a Simple Moving Averages plot
# of Morgan Stanley for the year 2015


bank_stocks["MS"].loc["2015-01-01":"2016-01-01"].ta_plot(study="sma")


# Use .ta_plot(study='boll') to create a Bollinger Band Plot for
# Bank of America for the year 2015


bank_stocks["BAC"].loc["2015-01-01":"2016-01-01"].ta_plot(study="boll")


# Lots of fascinating methods to explore and a great dataset
# to explore them with! As zi am into stocks I will definitely be using
# these methods in the future. Something wild is going on
# with GME at the moment so might be worth
# a similar analysis in the near future.
