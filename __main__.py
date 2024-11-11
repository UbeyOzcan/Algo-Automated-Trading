from utils.Data import DataFactory
from utils.Strategy import Strategy
from utils.Plot import PlotStrategy
import pandas as pd
pd.set_option('display.max_columns', None)

d = DataFactory(tickers=['AAPL'],
                period=['2024-1-01', '2024-10-31'],
                interval='1d')
df = d.get_stock_prices()
s = Strategy(data=df, tickers=['AAPL'])

ao = s.awesome_oscillator()
print(ao)
p = PlotStrategy(data=ao, tickers=['AAPL'])

fig = p.awesome_oscillator_plot()

print(ao[~ao['signal_ao_crossover|AAPL'].isnull()])