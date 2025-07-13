import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils import *
import pandas as pd

# --------------------------------------------
# Configure global dark theme for all plots.
# --------------------------------------------
plt.style.use('dark_background')

plt.rcParams.update({
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8
})

# Custom dark color palette
DARK_PALETTE = [
    "#00BCD4",  # Cyan
    "#0A7D36",  # Green
    "#8C0D39",  # Maroon
]

plt.rcParams["axes.prop_cycle"] = plt.cycler(color=DARK_PALETTE)
plt.rcParams["axes.edgecolor"] = "#888888"
plt.rcParams["xtick.color"] = "#CCCCCC"
plt.rcParams["ytick.color"] = "#CCCCCC"
plt.rcParams["grid.color"] = "#444444"

# --------------------------------------------
# Pie chart: Weekday vs Weekend split.
# --------------------------------------------
def plot_weekday_vs_weekend(data):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        data.values,
        labels=data.index,
        autopct='%1.1f%%',
        startangle=90,
        radius=0.8,
        colors=["#140081FF", "#00BCD4"]
    )
    ax.set_title("\n\nWeekday vs Weekend")
    fig.tight_layout()
    return fig

# --------------------------------------------
# Horizontal bar chart: Passengers by Time Slot.
# Shows peak hours.
# --------------------------------------------
def plot_passengers_by_timeslot(data):
    fig, ax = plt.subplots(figsize=(7, 8))

    ax.barh(data['Time Slot'].astype('str'), data['Passenger Count'])

    ax.set_title("Passengers by Time Slot")
    ax.set_xlabel("Passengers")
    ax.set_ylabel("Time Slot")
    ax.tick_params(axis='x', rotation=45)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format_inr(x)))

    for i, v in enumerate(data['Passenger Count']):
        ax.text(
            v - (0.01 * max(data['Passenger Count'])),
            i,
            format_inr(v),
            va='center',
            ha='right',
            color='black',
            fontsize=8,
            fontweight='bold'
        )

    fig.tight_layout()
    return fig

# --------------------------------------------
# Line chart: Yearly ridership trend.
# --------------------------------------------
def plot_yearly_ridership(data):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data['Year'], data['Passenger Count'], marker='o', linewidth=3)

    ax.set_title("Yearly Ridership")
    ax.set_ylabel("Passengers")
    ax.set_xlabel("Year")

    ax.set_xticks(data['Year'].tolist())
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format_inr(x)))

    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    return fig

# --------------------------------------------
# Horizontal bar chart: Top 10 Routes by Passengers.
# --------------------------------------------
def plot_passengers_by_route(data):
    fig, ax = plt.subplots(figsize=(10, 5))

    data = data.sort_values(ascending=True).tail(10)
    ax.barh(data.index, data.values, color='skyblue')

    ax.set_title("Top 10 Routes by Passengers")
    ax.set_xlabel("Passengers")
    ax.set_ylabel("Route")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format_inr(x)))

    for i, v in enumerate(data.values):
        ax.text(
            v - (0.01 * max(data.values)),
            i,
            format_inr(v),
            va='center',
            ha='right',
            color='black',
            fontsize=8,
            fontweight='bold'
        )

    fig.tight_layout()
    return fig

# --------------------------------------------
# Line chart: Monthly trend (Passengers or Fare).
# Supports multiple years.
# --------------------------------------------
def plot_monthly_trend(df, value_col, title):
    fig, ax = plt.subplots(figsize=(10, 6))

    for year in sorted(df['Year'].unique()):
        data_year = df[df['Year'] == year]
        ax.plot(data_year['Month'], data_year[value_col], marker='o', linewidth=3, label=str(year))

    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.set_ylabel(format_col_name(value_col))
    ax.set_xticks(range(1, 13))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format_inr(x)))
    ax.legend(title="Year", loc='upper right')

    fig.tight_layout()
    return fig

# --------------------------------------------
# Helper: Format y-axis labels based on column name.
# --------------------------------------------
def format_col_name(col):
    if col == 'Passenger Count':
        return "Passengers"
    elif col == 'Fare Collected':
        return "Fare Collected (₹)"
    else:
        return col

# --------------------------------------------
# Bar chart: Average passengers by weekday.
# --------------------------------------------
def plot_weekday_pattern(df_wday):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(df_wday['Weekday'], df_wday['Avg Passengers'])

    ax.set_title("Average Passengers by Weekday")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Avg Passengers")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format_inr(x)))

    for i, v in enumerate(df_wday['Avg Passengers']):
        ax.text(
            i,
            v + (0.01 * max(df_wday['Avg Passengers'])),
            format_inr(int(v)),
            ha='center',
            fontsize=8,
            fontweight='bold'
        )

    fig.tight_layout()
    return fig

# --------------------------------------------
# Horizontal bar chart: Top 10 Routes by Fare Collected.
# --------------------------------------------
def plot_fare_by_route(df_route):
    fig, ax = plt.subplots(figsize=(8, 5))

    if isinstance(df_route, pd.Series):
        df_route = df_route.reset_index()
        df_route.columns = ['Route', 'Fare Collected']

    df_route = df_route.sort_values('Fare Collected', ascending=True).tail(10)

    ax.barh(df_route['Route'], df_route['Fare Collected'])
    ax.set_title("Top 10 Routes by Fare Collected")
    ax.set_xlabel("Fare Collected (₹)")
    ax.set_ylabel("Route")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format_inr(x)))

    for i, v in enumerate(df_route['Fare Collected']):
        ax.text(
            v - (0.01 * max(df_route['Fare Collected'])),
            i,
            f'₹{format_inr(v)}',
            va='center',
            ha='right',
            color='black',
            fontsize=9,
            fontweight='bold'
        )

    fig.tight_layout()
    return fig

# --------------------------------------------
# Horizontal bar chart: Top 10 Stations by Fare Collected.
# --------------------------------------------
def plot_fare_by_station(df_station):
    fig, ax = plt.subplots(figsize=(8, 5))

    if isinstance(df_station, pd.Series):
        df_station = df_station.reset_index()
        df_station.columns = ['Boarding Station', 'Fare Collected']

    df_station = df_station.sort_values('Fare Collected', ascending=True).tail(10)

    ax.barh(df_station['Boarding Station'], df_station['Fare Collected'])
    ax.set_title("Top 10 Stations by Fare Collected")
    ax.set_xlabel("Fare Collected (₹)")
    ax.set_ylabel("Boarding Station")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format_inr(x)))

    for i, v in enumerate(df_station['Fare Collected']):
        ax.text(
            v - (0.01 * max(df_station['Fare Collected'])),
            i,
            f'₹{format_inr(v)}',
            va='center',
            ha='right',
            color='black',
            fontsize=9,
            fontweight='bold'
        )

    fig.tight_layout()
    return fig