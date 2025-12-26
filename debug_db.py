import sqlite3
import os
import pandas as pd

DB = os.path.join("data", "war.db")

print('DB path:', DB)
print('Exists:', os.path.exists(DB))

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('Tables:', tables)

for t in tables:
    try:
        cnt = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    except Exception as e:
        cnt = f'ERROR: {e}'
    print(f'{t}: {cnt}')

print('\nSample casualties (up to 10 rows):')
try:
    df = pd.read_sql('SELECT * FROM casualties LIMIT 10', conn)
    print(df)
except Exception as e:
    print('Unable to read casualties table:', e)

conn.close()
