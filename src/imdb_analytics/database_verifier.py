import os
import sqlite3

from imdb_analytics.database_builder import DB_PATH


def rowCounts() -> dict[str, int]:
    """ Function to count rows of every table in the db; read-only """
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")]
        return {table: conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0] for table in tables}
    finally:
        conn.close()

def report(counts: dict[str, int], dbSize: int) -> str:
    """ Markdown report about the database """
    lines = ["## IMDB database", "", "| table | rows |", "|---|---:|"]
    lines += [f"| {table} | {rows:,} " for table, rows in counts.items()]
    lines += ["", f"Database size: {dbSize / 1e9:.2f} GB"]
    return "\n".join(lines)

def main() -> None:
    if not os.PATH.EXISTS(DB_PATH):
        raise SystemExit(f"No database found at {DB_PATH}")
    
    counts = rowCounts()
    log = report(counts, os.path.getsize(DB_PATH))
    print(log)

if __name__ == "__main__":
    main()