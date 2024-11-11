from ta import momentum
import pandas as pd


class Strategy:
    def __init__(self, data: pd.DataFrame, tickers: list):
        self.data = data
        self.tickers = tickers

    def awesome_oscillator(self) -> pd.DataFrame:
        aw_osc_df = momentum.awesome_oscillator(
            high=self.data[f'High|{self.tickers[0]}'],
            low=self.data[f'Low|{self.tickers[0]}']).dropna()
        aw_osc_df = pd.DataFrame(aw_osc_df)
        aw_osc_df.columns = [f'ao|{self.tickers[0]}']
        self.data = self.data.join(aw_osc_df)
        self.data = self.data.dropna().reset_index()
        self.data[f'signal_ao_crossover|{self.tickers[0]}'] = None
        for i in range(1, len(self.data)):
            if self.data.loc[i, f'ao|{self.tickers[0]}'] < 0 < self.data.loc[i - 1, f'ao|{self.tickers[0]}']:
                self.data.loc[i, f'signal_ao_crossover|{self.tickers[0]}'] = 'Buy'
            elif self.data.loc[i, f'ao|{self.tickers[0]}'] > 0 > self.data.loc[i - 1, f'ao|{self.tickers[0]}']:
                self.data.loc[i, f'signal_ao_crossover|{self.tickers[0]}'] = 'Sell'

        return self.data
