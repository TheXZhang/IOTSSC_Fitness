import pandas as pd
import datetime as dt


columns=['date','time','username','wrist','activity','acceleration_x','acceleration_y','acceleration_z','gyro_x','gyro_y','gyro_z']

df = pd.read_csv('dataset.csv', names=columns, header=0)


date_time_df=pd.to_datetime(df['date'],format='%Y-%m-%d')

hours=df['time'].apply(lambda x: x[:-3])

hour_df=pd.to_datetime(hours,format='%H:%M:%S:%f')

df['hour']=hour_df.dt.hour
df['minutes']=hour_df.dt.minute
df['seconds']=hour_df.dt.second
df['microsecond']=hour_df.dt.microsecond

df['ordinal_time']=date_time_df.apply(dt.datetime.toordinal)

df.to_csv("new_dataset.csv", index=False)


