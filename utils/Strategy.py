import pandas as pd


class Strategy:
    def __init__(self, tickers: list, trade_value: int):
        self.trade_value = trade_value
        self.tickers = tickers

    def crossover(self, df_cross: pd.DataFrame) -> dict:
        current_trade = {}
        trades = []
        df_cross[f'signal_ao_crossover|{self.tickers[0]}'] = None
        for i in range(len(df_cross) - 1):
            if df_cross.loc[i + 1, f'ao|{self.tickers[0]}'] > 0 > df_cross.loc[i, f'ao|{self.tickers[0]}'] and len(
                    current_trade) != 0:
                df_cross.loc[i + 1, f'signal_ao_crossover|{self.tickers[0]}'] = 'Sell'
                trades.append({
                    "entry_price": current_trade["entry_price"],
                    "entry_time": current_trade["entry_time"],
                    "trade_size": current_trade["remaining_size"],
                    "exit_price": df_cross.iloc[i + 1][f'Open|{self.tickers[0]}'],
                    "exit_time": df_cross.iloc[i + 1].Date,
                    "profit_pct": (df_cross.iloc[i + 1][f'Open|{self.tickers[0]}'] / current_trade["entry_price"]) - 1,
                })

                current_trade = {}
            elif df_cross.loc[i + 1, f'ao|{self.tickers[0]}'] < 0 < df_cross.loc[i, f'ao|{self.tickers[0]}'] and len(
                    current_trade) == 0:
                df_cross.loc[i + 1, f'signal_ao_crossover|{self.tickers[0]}'] = 'Buy'
                current_trade["entry_price"] = df_cross.iloc[i + 1][f'Open|{self.tickers[0]}']
                current_trade["entry_time"] = df_cross.iloc[i + 1].Date
                current_trade["initial_size"] = self.trade_value / current_trade["entry_price"]
                current_trade["remaining_size"] = current_trade["initial_size"]
        trades = pd.DataFrame(trades)
        return {'trades': trades}

    def saucers(self, df_saucers: pd.DataFrame) -> dict:
        current_trade = {}
        trades = []
        df_saucers[f'signal_ao_saucers|{self.tickers[0]}'] = None

        # Assign colors based on AO values
        df_saucers[f'color ao|{self.tickers[0]}'] = 'green'

        for i in range(1, len(df_saucers)):
            if df_saucers.loc[i, f'ao|{self.tickers[0]}'] <= df_saucers.loc[i - 1, f'ao|{self.tickers[0]}']:
                df_saucers.loc[i, f'color ao|{self.tickers[0]}'] = 'red'

        for i in range(2, len(df_saucers)):
            # Sell signal
            if (df_saucers.loc[i - 2, f'color ao|{self.tickers[0]}'] == 'green' and df_saucers.loc[i - 1, f'color ao|{self.tickers[0]}'] == 'green' and
                    df_saucers.loc[i, f'color ao|{self.tickers[0]}'] == 'red' and df_saucers.loc[i - 1, f'ao|{self.tickers[0]}'] > df_saucers.loc[
                        i - 2, f'ao|{self.tickers[0]}'] and df_saucers.loc[i - 2, f'ao|{self.tickers[0]}'] < 0 and df_saucers.loc[
                        i - 1, f'ao|{self.tickers[0]}'] < 0 and
                    df_saucers.loc[i, f'ao|{self.tickers[0]}'] < 0 and len(current_trade) != 0):
                df_saucers.loc[i + 1, f'signal_ao_saucers|{self.tickers[0]}'] = 'Sell'
                trades.append({
                    "entry_price": current_trade["entry_price"],
                    "entry_time": current_trade["entry_time"],
                    "trade_size": current_trade["remaining_size"],
                    "exit_price": df_saucers.iloc[i + 1][f'Open|{self.tickers[0]}'],
                    "exit_time": df_saucers.iloc[i + 1].Date,
                    "profit_pct": (df_saucers.iloc[i + 1][f'Open|{self.tickers[0]}'] / current_trade["entry_price"]) - 1,
                })
                current_trade = {}
            elif (df_saucers.loc[i - 2, f'color ao|{self.tickers[0]}'] == 'red' and df_saucers.loc[i - 1, f'color ao|{self.tickers[0]}'] == 'red' and
                  df_saucers.loc[i, f'color ao|{self.tickers[0]}'] == 'green' and df_saucers.loc[i - 1, f'ao|{self.tickers[0]}'] < df_saucers.loc[
                      i - 2, f'ao|{self.tickers[0]}'] and df_saucers.loc[i - 2, f'ao|{self.tickers[0]}'] > 0 and df_saucers.loc[
                      i - 1, f'ao|{self.tickers[0]}'] > 0 and
                  df_saucers.loc[i, f'ao|{self.tickers[0]}'] > 0 and len(current_trade) == 0):
                df_saucers.loc[i + 1, f'signal_ao_saucers|{self.tickers[0]}'] = 'Buy'
                current_trade["entry_price"] = df_saucers.iloc[i + 1][f'Open|{self.tickers[0]}']
                current_trade["entry_time"] = df_saucers.iloc[i + 1].Date
                current_trade["initial_size"] = self.trade_value / current_trade["entry_price"]
                current_trade["remaining_size"] = current_trade["initial_size"]

        trades = pd.DataFrame(trades)
        return {'trades': trades}
