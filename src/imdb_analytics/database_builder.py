import os
import sqlite3

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "imdb.db")
CHUNK_SIZE = 500_000
KEY_COLUMNS = {"tconst", "nconst", "titleId", "parentTconst"}

def tableName(filename: str) -> str:
    """ title.basics.tsv.gz (filename) -> title_basics (name of table in db) """
    return filename.removesuffix(".gz").removesuffix(".tsv").replace(".", "_")

def readChunks(path: str):
    return pd.read_csv(path, sep="\t", na_values=r"\N", keep_default_na=False, quoting=3, dtype_backend="numpy_nullable", chunksize=CHUNK_SIZE)

def loadTable(conn: sqlite3.Connection, table: str, path: str) -> None:
    rows = 0
    for i, chunk in enumerate(readChunks(path)):
        chunk.to_sql(table, conn, if_exists="replace" if i == 0 else "append", index=False)
        rows += len(chunk)
        print(f"\r {table}: {rows:,} rows", end="", flush=True)
    print()


def indexKeys(conn: sqlite3.Connection, table: str) -> None:
    columns = [row[1] for row in conn.execute(f'PRAGMA table_info("{table}")')]
    for column in KEY_COLUMNS.intersection(columns):
        conn.execute(f'CREATE INDEX "idx_{table}_{column}" ON "{table}" ("{column}")')

def main() -> None:
    files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith((".tsv", ".tsv.gz")))
    if not files:
        raise SystemExit(f"No .tsv files in {DATA_DIR}")
    
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA journal_mode = OFF")
        conn.execute("PRAGMA synchronos = OFF") # if a run is interrupted we delete the imdb.db and rerun

        for filename in files:
            table = tableName(filename)
            loadTable(conn, table, os.path.join(DATA_DIR, filename))
            indexKeys(conn, table)
        conn.commit()
    finally:
        conn.close() # Used finally because we need to always close the connection, and with finally it is guaranted to be executed 
    
    print(f"Done: {len(files)} tables in {DB_PATH}")

if __name__ == "__main__":
    main()