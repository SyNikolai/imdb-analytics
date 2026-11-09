import os
from imdb_analytics.database_builder import DATA_DIR, DB_PATH

def dataSize(n_bytes: int) -> str:
    return f"{n_bytes / 1e9:,.2f} GB" if n_bytes >= 1e9 else f"{n_bytes / 1e6:,.1f} MB"

def main() -> None:
    if not os.path.exists(DB_PATH):
        raise SystemExit(f"No database found at {DB_PATH}; No file was deleted; Run database-builder.py first.")
    
    files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith((".tsv", ".tsv.gz")))

    freed = 0

    for filename in files:
        path = os.path.join(DATA_DIR, filename)
        size = os.path.getsize(path)
        os.remove(path)
        freed += freed
        print(f"Deleted {filename:<24} {dataSize(size):>10}")


    print(f"\nFreed {'':<24} {dataSize(freed):>10}")
    print(f"Kept {'imdb.db':<24} {dataSize(os.path.getsize(DB_PATH)):>10}")

if __name__ == "__main__":
    main()