import pandas as pd
import os

# file_type = "run"
file_type = "dwell"

time_step = 15
direction = 1

current_folder = os.path.abspath('')
dataSet_location = os.path.join(current_folder,'Datasets')

files = []
for i in range(1,4):
    filename = f"avg_{file_type}{i}_{time_step}min_dir{direction}.csv"
    file_address = os.path.join(dataSet_location,filename)
    files.append(file_address)

df1 = pd.read_csv(files[0])
df2 = pd.read_csv(files[1])
df3 = pd.read_csv(files[2])

overall_df = pd.concat([df1, df2, df3], axis=0)
overall_df['date'] = pd.to_datetime(overall_df['date'])

overall_df = overall_df.sort_values(by='date', ascending=True)

newfile = f"avg_{file_type}_5min_dir{direction}v2.csv"
processed_data_file = os.path.join(dataSet_location, newfile)

overall_df.to_csv(processed_data_file,index=False)
