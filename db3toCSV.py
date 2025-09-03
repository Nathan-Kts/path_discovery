#!/usr/bin/env python3
import sys
import duckdb
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python export_duckdb_to_csv.py <db_file.duckdb> [out_dir]")
        sys.exit(1)
    db_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "csv_export"

    con = duckdb.connect(db_path)  # opens DuckDB database file
    # Export every table in the DB to CSV files into out_dir
    con.execute(f"EXPORT DATABASE '{Path(out_dir).as_posix()}' (FORMAT csv)")
    print(f"Exported to {out_dir}")

if __name__ == "__main__":
    main()
