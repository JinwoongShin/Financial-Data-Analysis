import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import FinanceDataReader as fdr
from pandas_datareader import data as pdr
import yfinance as yf

df_nasdaq = pdr.get_data_yahoo('^ixic', '20071010', '20221112')
df_nasdaq.head()
# ohlcv : Open Hign Low Close Vulume