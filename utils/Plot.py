import plotly.graph_objects as go
import pandas as pd


class PlotStrategy:
    def __init__(self, data: pd.DataFrame, tickers: list):
        self.data = data
        self.tickers = tickers

    def awesome_oscillator_plot(self) -> go.Figure:

        # Assign colors based on AO values
        self.data[f'color ao|{self.tickers[0]}'] = 'green'

        for i in range(1, len(self.data)):
            if self.data.loc[i, f'ao|{self.tickers[0]}'] <= self.data.loc[i - 1, f'ao|{self.tickers[0]}']:
                self.data.loc[i, f'color ao|{self.tickers[0]}'] = 'red'

        # Create a bar plot with improved design
        fig = go.Figure()

        # Add bars with colors based on 'color' column
        fig.add_trace(go.Bar(
            x=self.data.Date,
            y=self.data[f'ao|{self.tickers[0]}'],
            marker_color=self.data[f'color ao|{self.tickers[0]}'],
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
