# Voi testata miltä data näyttää x määrällä rivejä

import sqlite3, pandas as pd

con = sqlite3.connect("data/stream.db")
df = pd.read_sql("SELECT * FROM deliveries LIMIT 12", con)
print(df)