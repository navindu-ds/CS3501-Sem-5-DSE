import pandas as pd

dataset = pd.read_csv("bus_running_times_feature_added_all.csv")

# groupby for number of unique buses travelled on the day of the week and hour of day
df_count_week_hour = dataset.groupby(['day_of_week','hour_of_day']).trip_id.nunique()

# number of days recorded for each of the week
df_count_date = dataset.groupby(['day_of_week']).date.nunique()

data = (round(df_count_week_hour / df_count_date)).unstack()

data.to_csv("AvgBuses.csv")