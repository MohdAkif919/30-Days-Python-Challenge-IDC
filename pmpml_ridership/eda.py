import pandas as pd
import utils

# --------------------------------------------
# Load and prepare data from uploaded CSV.
# Handles date parsing, fills missing values,
# and derives helper columns for analysis.
# --------------------------------------------
def load_and_clean_data(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig')

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()

    df['Passenger Count'] = df['Passenger Count'].fillna(0)

    df['Day Type'] = pd.to_datetime(df['Date']).dt.dayofweek.apply(
        lambda x: 'Weekend' if x >= 5 else 'Weekday'
    )

    df['Time Slot'] = df['Time Slot'].apply(utils.format_timeslot)

    return df

# --------------------------------------------
# Compute total number of passengers.
# --------------------------------------------
def total_passengers(df):
    return int(df['Passenger Count'].sum())

# --------------------------------------------
# Compute total fare collected.
# --------------------------------------------
def total_fare(df):
    return round(df['Fare'].sum(), 2)

# --------------------------------------------
# Show daily ridership trend.
# Total passengers per day.
# --------------------------------------------
def daily_ridership(df):
    return df.groupby('Date')['Passenger Count'].sum()

# --------------------------------------------
# Aggregate passengers by weekday vs weekend.
# Useful for high-level overview.
# --------------------------------------------
def weekday_vs_weekend(df):
    return df.groupby('Day Type')['Passenger Count'].sum()

# --------------------------------------------
# Calculate yearly ridership trend.
# --------------------------------------------
def yearly_ridership(df):
    df_year = df.groupby('Year')['Passenger Count'].sum().reset_index()
    df_year.columns = ['Year', 'Passenger Count']
    return df_year

# --------------------------------------------
# Calculate yearly fare trend.
# --------------------------------------------
def yearly_fare(df):
    df_year = df.groupby('Year')['Fare'].sum().reset_index()
    df_year.columns = ['Year', 'Fare Collected']
    return df_year

# --------------------------------------------
# Analyze monthly trend for passengers.
# Shows seasonality across years.
# --------------------------------------------
def monthly_passenger_trend(df):
    df_monthly = df.groupby(['Year', 'Month'], observed=False)['Passenger Count'].sum().reset_index()
    df_monthly.columns = ['Year', 'Month', 'Passenger Count']

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df_monthly['Month'] = pd.Categorical(df_monthly['Month'], categories=month_order, ordered=True)

    df_monthly = df_monthly.sort_values(['Year', 'Month'])

    return df_monthly

# --------------------------------------------
# Analyze monthly trend for fare collected.
# --------------------------------------------
def monthly_fare_trend(df):
    df_monthly = df.groupby(['Year', 'Month'], observed=False)['Fare'].sum().reset_index()
    df_monthly.columns = ['Year', 'Month', 'Fare Collected']

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df_monthly['Month'] = pd.Categorical(df_monthly['Month'], categories=month_order, ordered=True)

    df_monthly = df_monthly.sort_values(['Year', 'Month'])

    return df_monthly

# --------------------------------------------
# Average passengers by day of the week.
# Highlights patterns on specific weekdays.
# --------------------------------------------
def weekday_pattern(df):
    df['Weekday'] = pd.to_datetime(df['Date']).dt.day_name()

    df_wday = df.groupby('Weekday')['Passenger Count'].mean().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ).reset_index(name='Avg Passengers')

    return df_wday

# --------------------------------------------
# Aggregate passengers by time slot.
# Helps identify peak hours.
# --------------------------------------------
def peak_time_slots(df):
    grouped = df.groupby("Time Slot")["Passenger Count"].sum().reset_index()

    TIME_SLOT_ORDER = {
        '5:00AM - 6:00AM': 1,  '6:00AM - 7:00AM': 2,  '7:00AM - 8:00AM': 3,
        '8:00AM - 9:00AM': 4,  '9:00AM - 10:00AM': 5, '10:00AM - 11:00AM': 6,
        '11:00AM - 12:00PM': 7,'12:00PM - 1:00PM': 8,'1:00PM - 2:00PM': 9,
        '2:00PM - 3:00PM': 10, '3:00PM - 4:00PM': 11,'4:00PM - 5:00PM': 12,
        '5:00PM - 6:00PM': 13, '6:00PM - 7:00PM': 14,'7:00PM - 8:00PM': 15,
        '8:00PM - 9:00PM': 16, '9:00PM - 10:00PM': 17,'10:00PM - 11:00PM': 18
    }

    grouped['SlotOrder'] = grouped['Time Slot'].map(TIME_SLOT_ORDER)
    grouped = grouped.dropna(subset=['SlotOrder'])
    grouped = grouped.sort_values('SlotOrder')

    return grouped.drop(columns=['SlotOrder']).iloc[::-1]

# --------------------------------------------
# Aggregate passengers by route.
# Highlights most popular routes.
# --------------------------------------------
def top_routes(df):
    return df.groupby("Route")["Passenger Count"].sum().sort_values(ascending=False)

# --------------------------------------------
# Aggregate fare by route.
# --------------------------------------------
def fare_by_route(df):
    df_route = df.groupby('Route')['Fare'].sum().reset_index()
    df_route.columns = ['Route', 'Fare Collected']
    return df_route.sort_values(by='Fare Collected', ascending=False)

# --------------------------------------------
# Aggregate passengers by boarding station.
# Shows busiest stations.
# --------------------------------------------
def busiest_stations(df):
    return df.groupby("Boarding Station")["Passenger Count"].sum().sort_values(ascending=False)

# --------------------------------------------
# Aggregate fare by boarding station.
# --------------------------------------------
def fare_by_station(df):
    df_station = df.groupby('Boarding Station')['Fare'].sum().reset_index()
    df_station.columns = ['Boarding Station', 'Fare Collected']
    return df_station.sort_values(by='Fare Collected', ascending=False)

# --------------------------------------------
# Route vs time slot matrix.
# Shows peak slots for each route.
# --------------------------------------------
def route_peak_timeslot(df):
    return pd.pivot_table(
        df, index='Route', columns='Time Slot',
        values='Passenger Count', aggfunc='sum'
    ).fillna(0)

# --------------------------------------------
# Route vs weekday/weekend matrix.
# --------------------------------------------
def route_weekday_weekend(df):
    return pd.pivot_table(
        df, index='Route', columns='Day Type',
        values='Passenger Count', aggfunc='sum'
    ).fillna(0)

# --------------------------------------------
# Station vs routes matrix.
# Shows how routes connect at stations.
# --------------------------------------------
def station_vs_routes(df):
    return pd.pivot_table(
        df, index='Boarding Station', columns='Route',
        values='Passenger Count', aggfunc='sum'
    ).fillna(0)

# --------------------------------------------
# Generate high-level ridership insight.
# --------------------------------------------
def generate_overview_insight(df):
    if df.empty:
        return "No data available to generate insights."

    total_passengers = df['Passenger Count'].sum()

    if 'Day Type' not in df.columns:
        df['Day Type'] = pd.to_datetime(df['Date']).dt.dayofweek.apply(
            lambda x: 'Weekend' if x >= 5 else 'Weekday'
        )

    weekday_count = df[df['Day Type'] == 'Weekday']['Passenger Count'].sum()
    weekend_count = df[df['Day Type'] == 'Weekend']['Passenger Count'].sum()

    weekday_pct = (weekday_count / total_passengers) * 100 if total_passengers else 0
    weekend_pct = 100 - weekday_pct

    peak_pct = None
    peak_slots = []

    if 'Time Slot' in df.columns:
        slot_counts = df.groupby('Time Slot')['Passenger Count'].sum().sort_values(ascending=False)
        top_slots = slot_counts.head(2)
        peak_count = top_slots.sum()
        peak_slots = top_slots.index.tolist()
        peak_pct = (peak_count / total_passengers) * 100 if total_passengers else 0

    insight_lines = [
        f"- Weekdays account for ~{weekday_pct:.1f}% of total ridership.",
        f"- Weekends account for ~{weekend_pct:.1f}% of total ridership."
    ]

    if peak_pct is not None and peak_slots:
        slots_text = ", ".join(peak_slots)
        insight_lines.append(f"- Peak slots ({slots_text}) cover ~{peak_pct:.1f}% of passengers.")

    return "\n".join(insight_lines)

# --------------------------------------------
# Generate insight for routes.
# Highlights top routes and peak slot for busiest.
# --------------------------------------------
def generate_routes_insight(df):
    if df.empty:
        return "No data available for routes insights."

    total_passengers = df['Passenger Count'].sum()
    route_counts = df.groupby('Route')['Passenger Count'].sum().sort_values(ascending=False)

    top_routes = route_counts.head(3)
    top_routes_list = top_routes.index.tolist()
    top_routes_pct = (top_routes.sum() / total_passengers) * 100 if total_passengers else 0

    insight = (
        f"- Top routes ({', '.join(top_routes_list)}) account for ~{top_routes_pct:.1f}% of total ridership."
    )

    if 'Time Slot' in df.columns:
        top_route = top_routes.index[0]
        route_df = df[df['Route'] == top_route]
        slot_counts = route_df.groupby('Time Slot')['Passenger Count'].sum().sort_values(ascending=False)
        if not slot_counts.empty:
            peak_slot = slot_counts.index[0]
            insight += f"\n- For {top_route}, the busiest slot is {peak_slot}."

    return insight

# --------------------------------------------
# Generate insight for stations.
# Highlights top stations and connected routes.
# --------------------------------------------
def generate_stations_insight(df):
    if df.empty:
        return "No data available for stations insights."

    total_passengers = df['Passenger Count'].sum()
    station_counts = df.groupby('Boarding Station')['Passenger Count'].sum().sort_values(ascending=False)

    top_stations = station_counts.head(3)
    top_stations_list = top_stations.index.tolist()
    top_stations_pct = (top_stations.sum() / total_passengers) * 100 if total_passengers else 0

    insight = (
        f"- Top stations ({', '.join(top_stations_list)}) handle ~{top_stations_pct:.1f}% of total ridership."
    )

    if 'Route' in df.columns:
        top_station = top_stations.index[0]
        routes = df[df['Boarding Station'] == top_station]['Route'].nunique()
        insight += f"\n- {top_station} connects to {routes} different routes."

    return insight

# --------------------------------------------
# Generate trends insight combining multiple facets.
# --------------------------------------------
def generate_trends_insight(df_monthly_pass, df_monthly_fare, df_yearly_pass, df_weekday=None):
    if df_monthly_pass.empty or df_yearly_pass.empty:
        return "No data available for trends insights."

    insights = []

    total_pass = df_monthly_pass['Passenger Count'].sum()
    month_totals = df_monthly_pass.groupby('Month', observed=False)['Passenger Count'].sum().reindex(
        ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]
    ).dropna()

    if not month_totals.empty:
        top_month = month_totals.idxmax()
        top_value = month_totals.max()
        month_pct = (top_value / total_pass) * 100 if total_pass else 0
        insights.append(f"- {top_month} is the busiest month (~{month_pct:.1f}%) for passengers.")

    if df_monthly_fare is not None and not df_monthly_fare.empty:
        fare_col = next((col for col in ['Fare Collected', 'Fare'] if col in df_monthly_fare.columns), None)
        if fare_col:
            total_fare = df_monthly_fare[fare_col].sum()
            fare_totals = df_monthly_fare.groupby('Month', observed=False)[fare_col].sum().reindex(
                ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
            ).dropna()
            if not fare_totals.empty:
                top_fare_month = fare_totals.idxmax()
                top_fare_value = fare_totals.max()
                fare_pct = (top_fare_value / total_fare) * 100 if total_fare else 0
                insights.append(f"- {top_fare_month} contributes the most to fare (~{fare_pct:.1f}%).")

    df_yearly_sorted = df_yearly_pass.sort_values('Year')
    if len(df_yearly_sorted) >= 2:
        last_year_val = df_yearly_sorted['Passenger Count'].iloc[-1]
        prev_year_val = df_yearly_sorted['Passenger Count'].iloc[-2]
        if prev_year_val != 0:
            yoy_change = ((last_year_val - prev_year_val) / prev_year_val) * 100
            trend = "increase" if yoy_change >= 0 else "decrease"
            insights.append(f"- There’s a {trend} of ~{abs(yoy_change):.1f}% in ridership compared to the previous year.")

    if df_weekday is not None and not df_weekday.empty:
        top_day_row = df_weekday.loc[df_weekday['Avg Passengers'].idxmax()]
        top_day = top_day_row['Weekday']
        insights.append(f"- {top_day} shows the highest average daily ridership.")

    return "\n".join(insights)

# --------------------------------------------
# Generate fare-specific insight.
# --------------------------------------------
def generate_fare_insight(df):
    if df.empty:
        return "No data available for fare insights."

    fare_col = next((col for col in ['Fare Collected', 'Fare'] if col in df.columns), None)
    if not fare_col:
        return "No fare column found."

    insights = []

    if 'Year' in df.columns:
        yearly_fare = df.groupby('Year')[fare_col].sum().sort_index()
        if len(yearly_fare) >= 2:
            last_year, prev_year = yearly_fare.index[-1], yearly_fare.index[-2]
            last_val, prev_val = yearly_fare.iloc[-1], yearly_fare.iloc[-2]
            if prev_val != 0:
                yoy_change = ((last_val - prev_val) / prev_val) * 100
                trend = "increase" if yoy_change >= 0 else "decrease"
                insights.append(f"- Yearly fare shows a {trend} of ~{abs(yoy_change):.1f}% compared to {prev_year}.")

    if 'Route' in df.columns:
        route_fare = df.groupby('Route')[fare_col].sum().sort_values(ascending=False)
        top_routes = route_fare.head(3)
        top_routes_list = top_routes.index.tolist()
        total_fare = df[fare_col].sum()
        top_routes_pct = (top_routes.sum() / total_fare) * 100 if total_fare else 0
        insights.append(f"- Top routes ({', '.join(top_routes_list)}) contribute ~{top_routes_pct:.1f}% of total fare.")

    if 'Boarding Station' in df.columns:
        station_fare = df.groupby('Boarding Station')[fare_col].sum().sort_values(ascending=False)
        top_stations = station_fare.head(3)
        top_stations_list = top_stations.index.tolist()
        total_fare = df[fare_col].sum()
        top_stations_pct = (top_stations.sum() / total_fare) * 100 if total_fare else 0
        insights.append(f"- Top stations ({', '.join(top_stations_list)}) handle ~{top_stations_pct:.1f}% of total fare.")

    return "\n".join(insights) if insights else "No insights generated due to missing data."