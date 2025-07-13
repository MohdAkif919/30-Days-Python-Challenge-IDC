# utils.py

# --------------------------------------------
# Format a number into Indian numbering style.
# Example: 123456789 -> 12,34,56,789
# --------------------------------------------
def format_inr(number):
    """
    Format a number into Indian numbering style: 12,34,56,789
    """
    num_str = str(int(number))
    last_three = num_str[-3:]
    other_numbers = num_str[:-3]

    if other_numbers != '':
        last_three = ',' + last_three

    res = ''
    while len(other_numbers) > 2:
        # Add commas every two digits for the lakhs and crores part
        res = ',' + other_numbers[-2:] + res
        other_numbers = other_numbers[:-2]

    res = other_numbers + res
    formatted = res + last_three
    return formatted

# --------------------------------------------
# Format all numeric columns in a DataFrame 
# into Indian number format.
# Returns a new DataFrame with formatted strings.
# --------------------------------------------
def format_dataframe_inr(df):
    """
    Apply Indian number format to all numeric columns in a DataFrame
    """
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].dtype in ['float64', 'int64']:
            df_copy[col] = df_copy[col].apply(format_inr)
    return df_copy

# --------------------------------------------
# Format a time slot string into standard AM/PM format.
# E.g., '5:00-6:00' -> '5:00AM - 6:00AM'
# If format fails, return original string.
# --------------------------------------------
def format_timeslot(ts):
    """
    Format a time slot string into 'H:00AM/PM - H:00AM/PM' format.
    """
    try:
        # Split slot into start and end times
        start, end = ts.split('-')
        start_hr = int(start.split(':')[0])
        end_hr = int(end.split(':')[0])

        # Determine AM/PM for start and end
        start_period = "AM" if start_hr < 12 else "PM"
        end_period = "AM" if end_hr < 12 else "PM"

        # Convert 24-hour to 12-hour format
        if start_hr == 0:
            start_hr = 12
        elif start_hr > 12:
            start_hr -= 12

        if end_hr == 0:
            end_hr = 12
        elif end_hr > 12:
            end_hr -= 12

        return f"{start_hr}:00{start_period} - {end_hr}:00{end_period}"

    except Exception:
        # If parsing fails, return the input unchanged
        return ts