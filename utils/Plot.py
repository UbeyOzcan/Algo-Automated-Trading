import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from datetime import timedelta


class PlotStrategy:
    def __init__(self, data: pd.DataFrame, tickers: list):
        self.data = data
        self.tickers = tickers

    def closing_price_plot(self) -> go.Figure:
        fig = go.Figure(data=[go.Candlestick(x=self.data.Date,
                                             open=self.data[f'Open|{self.tickers[0]}'],
                                             high=self.data[f'High|{self.tickers[0]}'],
                                             low=self.data[f'Low|{self.tickers[0]}'],
                                             close=self.data[f'Close|{self.tickers[0]}'],
                                             increasing_line_color='green',  # Candles that closed higher
                                             decreasing_line_color='red',  # Candles that closed lower
                                             showlegend=False
                                             )])

        # Customize layout
        fig.update_layout(
            title=f'Candlestick Chart for {self.tickers[0]}',
            xaxis_title='Date',
            yaxis_title='Price',
            template='plotly_white',  # Cleaner background
            xaxis_rangeslider_visible=False,  # Hide the range slider
            xaxis=dict(
                showgrid=True, gridcolor='lightgray', tickangle=-45,  # Tilt date labels for readability
            ),
            yaxis=dict(
                showgrid=True, gridcolor='lightgray',
            ),
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            hovermode='x unified',  # Display all data on the x-axis on hover
        )

        return fig

    def awesome_oscillator_plot(self) -> go.Figure:

        # Assign colors based on AO values
        self.data[f'color ao_cross|{self.tickers[0]}'] = 'green'

        for i in range(1, len(self.data)):
            if self.data.loc[i, f'ao|{self.tickers[0]}'] <= self.data.loc[i - 1, f'ao|{self.tickers[0]}']:
                self.data.loc[i, f'color ao_cross|{self.tickers[0]}'] = 'red'

        # Create a bar plot with improved design
        fig = go.Figure()

        # Add bars with colors based on 'color' column
        fig.add_trace(go.Bar(
            x=self.data.Date,
            y=self.data[f'ao|{self.tickers[0]}'],
            marker_color=self.data[f'color ao_cross|{self.tickers[0]}'],
            opacity=0.8,  # Make bars slightly transparent
            width=0.8  # Adjust bar width for better spacing
        ))

        # Update layout for improved design
        fig.update_layout(
            title=dict(
                text=f'Awesome Oscillator with Enhanced Visualization for {self.tickers[0]}',
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

    def entry_exist_plot(self, trades_df: pd.DataFrame) -> go.Figure:
        if trades_df.empty:
            return go.Figure()
        else:
            # Create subplots with specified row heights and shared x-axis
            fig = go.Figure()
            # Candlestick chart (first row)
            fig.add_trace(go.Candlestick(
                x=self.data.Date,
                open=self.data[f'Open|{self.tickers[0]}'],
                high=self.data[f'High|{self.tickers[0]}'],
                low=self.data[f'Low|{self.tickers[0]}'],
                close=self.data[f'Close|{self.tickers[0]}'],
                increasing_line_color='rgba(107,107,107,0.8)',
                decreasing_line_color='rgba(210,210,210,0.8)',
                name=f'{self.tickers[0]}'
            ))

            # Scatter plots for Entries and Exits (first row)
            fig.add_trace(go.Scatter(
                x=trades_df.entry_time,
                y=trades_df.entry_price,
                mode="markers",
                customdata=trades_df,
                marker_symbol="diamond-dot",
                marker_size=13,
                marker_line_width=2,
                marker_line_color="rgba(0,0,0,0.7)",
                marker_color="rgba(0,255,0,0.7)",
                hovertemplate="Entry Time: %{customdata[1]}<br>Entry Price: %{y:.2f}<br>Size: %{customdata[2]:.5f}<br>Profit_pct: %{customdata[5]:.3f}",
                name="Entries"
            ))

            fig.add_trace(go.Scatter(
                x=trades_df.exit_time,
                y=trades_df.exit_price,
                mode="markers",
                customdata=trades_df,
                marker_symbol="diamond-dot",
                marker_size=13,
                marker_line_width=2,
                marker_line_color="rgba(0,0,0,0.7)",
                marker_color="rgba(255,0,0,0.7)",
                hovertemplate="Exit Time: %{customdata[4]}<br>Exit Price: %{y:.2f}<br>Size: %{customdata[2]:.5f}<br>Profit_pct: %{customdata[5]:.3f}",
                name="Exits"
            ))

            fig.update_layout(xaxis_rangeslider_visible=False)

            return fig
