import pandas as pd
import calendar

#reading dataset
ds = pd.read_csv('datasets/sanFran_clean.csv')


#maps dataset
dsmap = ds.district.value_counts()
ds_viz = pd.DataFrame(data=dsmap.values, index=dsmap.index, columns=['Count'])
ds_viz = ds_viz.reindex(["CENTRAL", "NORTHERN", "PARK", "SOUTHERN", "MISSION", "TENDERLOIN", "RICHMOND", "TARAVAL", "INGLESIDE", "BAYVIEW"])
ds_viz = ds_viz.reset_index()
ds_viz.rename({'index': 'Neighborhood', 'Count': 'Arrests'}, axis='columns', inplace=True)
ds_viz.to_csv('datasets/ds_viz.csv')


#dropdown dataset
ds_unique = ds[['day', 'district']]
ds_unique = ds_unique.groupby(["day", "district"]).size().reset_index(name="Crime Frequency")
ds_unique.to_csv('datasets/ds_unique.csv')


# table 3
ds3 = ds[['month', 'district']]
ds3 = ds3.groupby(["month", "district"]).size().reset_index(name="Crime Frequency")
ds3['month'] = ds3['month'].apply(lambda x: calendar.month_abbr[x])
ds3.to_csv('datasets/ds3.csv')


# table 4
ds4 = ds[['year', 'district']]
ds4 = ds4.groupby(["year", "district"]).size().reset_index(name="Crime Frequency")
ds4.to_csv('datasets/ds4.csv')


# table 5
ds5 = ds[ds.result != "NONE"]
ds5 = pd.DataFrame(ds5.result.value_counts()).reset_index()
ds5.to_csv('datasets/ds5.csv')