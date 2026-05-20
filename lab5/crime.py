print("start")

import pandas as pd
import os

file_path = "Crimes_-_2001_to_Present.csv"
output_path = "chicago_crimes_parquet"

print("loading csv")

df = pd.read_csv(
    file_path,
    low_memory=False,
    nrows=2000000
)

print("csv loaded")

print("removing duplicates")
df = df.drop_duplicates()

print("fixing dates")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("removing missing data")
df = df.dropna(subset=[
    "ID",
    "Case Number",
    "Date",
    "Primary Type",
    "Location Description"
])

print("removing wrong dates")
df = df[
    (df["Date"].dt.year >= 2001) &
    (df["Date"].dt.year <= pd.Timestamp.now().year)
]

print("filtering wrong coordinates")
df = df[
    (df["Latitude"].isna() | df["Latitude"].between(41.0, 43.0)) &
    (df["Longitude"].isna() | df["Longitude"].between(-88.5, -87.0))
]

print("creating time columns")
df["year"] = df["Date"].dt.year
df["month"] = df["Date"].dt.month
df["hour"] = df["Date"].dt.hour
df["day_of_week"] = df["Date"].dt.day_name()

def day_period(hour):
    if pd.isna(hour):
        return "unknown"
    if 0 <= hour < 6:
        return "night"
    elif 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "day"
    else:
        return "evening"

print("adding day period column using udf")
df["day_period"] = df["hour"].apply(day_period)

print("cache dataframe")
cached_df = df.copy()

print("creating small location table")

locations = pd.DataFrame({
    "Location Description": [
        "STREET",
        "SIDEWALK",
        "RESIDENCE",
        "APARTMENT",
        "SCHOOL",
        "CTA TRAIN",
        "CTA BUS"
    ],
    "location_group": [
        "public",
        "public",
        "private",
        "private",
        "school",
        "transport",
        "transport"
    ]
})

print("broadcast join simulation")
cached_df = cached_df.merge(
    locations,
    on="Location Description",
    how="left"
)

cached_df["location_group"] = cached_df["location_group"].fillna("other")

print("saving to parquet with year partition")

os.makedirs(output_path, exist_ok=True)

cached_df.to_parquet(
    output_path,
    engine="pyarrow",
    partition_cols=["year"],
    index=False
)

print("parquet saved")

print("\nanalysis 1: crimes by type")
query1 = (
    cached_df
    .groupby("Primary Type")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

print(query1.head(20))

print("\nexplain query1")
print("DataFrame -> groupby Primary Type -> count rows -> sort by count descending -> show top 20")

print("\nanalysis 2: crimes by location")
query2 = (
    cached_df
    .groupby("Location Description")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

print(query2.head(20))

print("\nexplain query2")
print("DataFrame -> groupby Location Description -> count rows -> sort by count descending -> show top 20")

print("\nanalysis 3: crimes by location group")
query3 = (
    cached_df
    .groupby("location_group")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

print(query3)

print("\nexplain query3")
print("DataFrame -> small table joined like broadcast -> groupby location_group -> count rows -> sort descending")

print("\nanalysis 4: crimes by year and month")
query4 = (
    cached_df
    .groupby(["year", "month"])
    .size()
    .reset_index(name="count")
    .sort_values(["year", "month"])
)

print(query4.head(100))

print("\nexplain query4")
print("DataFrame -> groupby year and month -> count rows -> sort by year and month")

print("\nanalysis 5: crimes by day period")
query5 = (
    cached_df
    .groupby("day_period")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

print(query5)

print("\nexplain query5")
print("DataFrame -> UDF creates day_period -> groupby day_period -> count rows -> sort descending")

print("\nanalysis 6: crimes by day of week")
query6 = (
    cached_df
    .groupby("day_of_week")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

print(query6)

print("\nexplain query6")
print("DataFrame -> groupby day_of_week -> count rows -> sort descending")

print("\nanalysis 7: top 5 crime types in each day period")

query7 = (
    cached_df
    .groupby(["day_period", "Primary Type"])
    .size()
    .reset_index(name="count")
)

query7["rank"] = query7.groupby("day_period")["count"].rank(
    method="dense",
    ascending=False
)

query7 = query7[query7["rank"] <= 5]

query7 = query7.sort_values(["day_period", "rank"])

print(query7)



print("\nfinished")