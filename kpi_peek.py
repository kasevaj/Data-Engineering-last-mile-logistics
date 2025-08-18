import sqlite3, pandas as pd

con = sqlite3.connect("data/stream.db")
df = pd.read_sql("SELECT * FROM deliveries LIMIT 5", con)
print(df.columns.tolist())
print(df.head())
con.close()

['id', 'Order_ID', 'Agent_Age', 'Agent_Rating', 'Store_Latitude', 'Store_Longitude', 'Drop_Latitude', 'Drop_Longitude', 'Order_Date', 'Order_Time', 'Pickup_Time', 'Weather', 'Traffic', 'Vehicle', 'Area', 'Delivery_Time', 'Category']