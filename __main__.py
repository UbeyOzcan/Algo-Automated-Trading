from utils.Data import DataFactory
from utils.Strategy import Strategy
from utils.Plot import PlotStrategy
import pandas as pd

for i in ['AAPL']:
    d = DataFactory(tickers=[i],
                    period=['2024-1-01', '2024-10-31'],
                    interval='1d')
    df = d.get_stock_prices()
    df = d.ao(df=df)
    s = Strategy(tickers=d.tickers, trade_value=100)
    ao_cross = s.crossover(df_cross=df)
    ao_saucers = s.saucers(df_saucers=df)
    p = PlotStrategy(data=df, tickers=d.tickers)
    with pd.ExcelWriter(f'Result_{i}.xlsx') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
        ao_cross['trades'].to_excel(writer, sheet_name='AO_Cross', index=False)
        ao_saucers['trades'].to_excel(writer, sheet_name='AO_Saucers', index=False)
    print('DataFrames are written to Excel File successfully.')
    p.awesome_oscillator_plot().show()
    p.entry_exist_plot(trades_df=ao_cross['trades']).show()
    p.entry_exist_plot(trades_df=ao_saucers['trades']).show()
