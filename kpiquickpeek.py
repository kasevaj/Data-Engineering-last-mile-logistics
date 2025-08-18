import sqlite3, pandas as pd

con = sqlite3.connect("data/stream.db")


query = """
SELECT
    *
FROM deliveries
"""
df = pd.read_sql(query, con)
con.close()

id_col = 'id'
order_id_col = 'Order_ID'
agent_age_col = 'Agent_Age'
agent_rating_col = 'Agent_Rating'
store_latitude_col = 'Store_Latitude'
store_longitude_col = 'Store_Longitude'
drop_latitude_col = 'Drop_Latitude'
drop_longitude_col = 'Drop_Longitude'
order_date_col = 'Order_Date' 
order_time_col = 'Order_Time' 
pickup_time_col = 'Pickup_Time' 
weather_col = 'Weather'
traffic_col = 'Traffic' 
vahicle_col = 'Vehicle' 
area_col = 'Area'
delivery_time_col = 'Delivery_Time' 
category_col = 'Category'

for c in [delivery_time_col, agent_rating_col]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")


total_orders = len(df)
avg_time = df[delivery_time_col].mean() if delivery_time_col in df else None
p90_time = df[delivery_time_col].quantile(0.90) if delivery_time_col in df else None
avg_rating = df[agent_rating_col].mean() if agent_rating_col in df else None
areas = df[area_col].nunique() if area_col in df else None


print("\n=== KPI:t ===")
print(f"Tilauksia yhteensä: {total_orders}")
if avg_time is not None:
    print(f"Keskimääräinen toimitusaika (min): {avg_time:.1f}")
    print(f"90. persentiili toimitusaika (min): {p90_time:.1f}")
if avg_rating is not None:
    print(f"Kuljettajan keskim. rating: {avg_rating:.2f}")
if areas is not None:
    print(f"Alueita: {areas}")

# Top alueet tilausmäärällä 
if area_col in df:
    print("\nTop alueet (tilaukset):")
    print(df[area_col].value_counts().head(5).to_string())

print("\nKeski-toimitusaika per Area")
print(df.groupby("Area")["Delivery_Time"].agg(["count","mean","median","quantile"]).rename(columns={"quantile":"p90"}))

print("\nSää x Liikenne (pivot)")
pv = df.pivot_table(values="Delivery_Time", index="Weather", columns="Traffic", aggfunc="mean")
print(pv.round(1))