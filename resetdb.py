# Tietokannan resetointiin jotta voi simuloida streamia.

import sqlite3
con = sqlite3.connect("data/stream.db")
con.execute("DELETE FROM deliveries")
con.commit()
con.close()
print("Tyhjennetty deliveries-taulu.")