import yfinance as yf
import pandas as pd
from ta import momentum


class DataFactory:
    def __init__(self, tickers: list, period: list, interval: str):
        self.tickers = tickers
        self.period = period
        self.interval = interval

    def get_stock_prices(self) -> pd.DataFrame:
        df = round(yf.download(self.tickers, self.period[0], self.period[1], interval=self.interval), 2)
        df.columns = df.columns.map('|'.join).str.strip('|')
        df.index = df.index.tz_localize(None)
        return df

    def ao(self, df: pd.DataFrame) -> pd.DataFrame:
        df_ao = momentum.awesome_oscillator(
            high=df[f'High|{self.tickers[0]}'],
            low=df[f'Low|{self.tickers[0]}']).dropna()
        df_ao = pd.DataFrame(df_ao)
        df_ao.columns = [f'ao|{self.tickers[0]}']
        df = df.join(df_ao)
        df = df.dropna().reset_index()
        return df
