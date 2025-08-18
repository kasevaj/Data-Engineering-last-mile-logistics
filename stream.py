# stream_to_sqlite.py
import csv, sqlite3, time
from pathlib import Path

DATA_DIR = Path("data/amazon")
DB_PATH = Path("data/stream.db")
TABLE = "deliveries"
BATCH = 20
SLEEP_SEC = 0.1           

def get_csv_path() -> Path:
    files = sorted(DATA_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"Ei csv-tiedostoja kansiossa {DATA_DIR.resolve()}")
    return files[0]

def ensure_table(conn: sqlite3.Connection, headers: list[str]):
    cols = ", ".join([f'"{h}" TEXT' for h in headers])
    conn.execute(f'CREATE TABLE IF NOT EXISTS {TABLE} (id INTEGER PRIMARY KEY AUTOINCREMENT, {cols})')
    conn.commit()

def insert_rows(conn: sqlite3.Connection, headers: list[str], rows: list[dict]):
    placeholders = ", ".join(["?"] * len(headers))
    cols = ", ".join([f'"{h}"' for h in headers])
    values = [[row.get(h) for h in headers] for row in rows]
    conn.executemany(f'INSERT INTO {TABLE} ({cols}) VALUES ({placeholders})', values)
    conn.commit()

def main():
    csv_path = get_csv_path()
    print("Streaming from:", csv_path)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    batch = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        if not headers:
            raise ValueError("CSV:stä ei löytynyt otsikkoriviä (header).")
        ensure_table(conn, headers)

        for i, row in enumerate(reader, start=1):
            # ohita täysin tyhjät rivit
            if not any(row.values()):
                continue

            batch.append(row)

            # simuloidaan streamiä
            if SLEEP_SEC:
                time.sleep(SLEEP_SEC)

            # kirjoita erissä
            if len(batch) >= BATCH:
                insert_rows(conn, headers, batch)
                print(f"→ kirjattu {i} riviä")
                batch.clear()

        # kirjoita mahdolliset loppuerät
        if batch:
            insert_rows(conn, headers, batch)
            print(f"→ kirjattu {i} riviä (valmis)")

    conn.close()
    print(f"OK ✔ SQLite: {DB_PATH.resolve()} taulu: {TABLE}")

if __name__ == "__main__":
    main()
