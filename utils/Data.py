import yfinance as yf
import pandas as pd
from ta import momentum
import plotly.graph_objects as go


class DataFactory:
    def __init__(self, ticker: list, period: list, interval: str):
        self.ticker = ticker
        self.period = period
        self.interval = interval

    def get_stock_price(self) -> pd.DataFrame:
        return round(yf.download(self.ticker, self.period[0], self.period[1], interval=self.interval), 2)

    def awesome_oscillator(self) -> pd.DataFrame:
        price_df = self.get_stock_price()
        aw_osc_df = momentum.awesome_oscillator(
            high=price_df['High'][self.ticker[0]],
            low=price_df['Low'][self.ticker[0]]).dropna().reset_index()
        aw_osc_df.columns = ['Datetime', 'ao']
        return aw_osc_df

    def awesome_oscillator_plot(self) -> go.Figure:
        df = self.awesome_oscillator()
        # Assign colors based on AO values
        df['color'] = 'green'
        for i in range(1, len(df)):
            if df.loc[i, 'ao'] <= df.loc[i - 1, 'ao']:
                df.loc[i, 'color'] = 'red'

        # Create a bar plot with improved design
        fig = go.Figure()

        # Add bars with colors based on 'color' column
        fig.add_trace(go.Bar(
            x=df['Datetime'],
            y=df['ao'],
            marker_color=df['color'],
            opacity=0.8,  # Make bars slightly transparent
            width=0.8  # Adjust bar width for better spacing
        ))

        # Update layout for improved design
        fig.update_layout(
            title=dict(
                text=f'Awesome Oscillator with Enhanced Visualization for {self.ticker[0]}',
                font=dict(size=24, family="Arial", color="black"),
                x=0.5  # Center-align the title
            ),
            xaxis=dict(
                type="category",
                title="Date",
                titlefont=dict(size=18),
                tickformat="%Y-%m-%d %H:%M",
                tickangle=45,  # Rotate labels for readability
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                title="AO",
                titlefont=dict(size=18),
                gridcolor="LightGray"
            ),
            plot_bgcolor="whitesmoke",  # Change background color for contrast
            width=1200,
            height=600,
        )

        # Add subtle gridlines for improved readability
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

        return fig


# Initialize DataFactory with ticker and date range
p = DataFactory(ticker=['MSFT'], period=['2024-10-01', '2024-10-31'], interval='1h')
fig = p.awesome_oscillator_plot()

fig.show()

# Initialize DataFactory with ticker and date range
p = DataFactory(ticker=['MSFT'], period=['2024-1-01', '2024-10-31'], interval='1d')
fig = p.awesome_oscillator_plot()

fig.show()
