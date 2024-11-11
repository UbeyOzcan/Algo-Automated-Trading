import yfinance as yf
import pandas as pd




class DataFactory:
    def __init__(self, tickers: list, period: list, interval: str):
        self.tickers = tickers
        self.period = period
        self.interval = interval

    def get_stock_prices(self) -> pd.DataFrame:
        df = round(yf.download(self.tickers, self.period[0], self.period[1], interval=self.interval), 2)
        df.columns = df.columns.map('|'.join).str.strip('|')
        return df


