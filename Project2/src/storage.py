from pathlib import Path
import sqlite3

import pandas as pd


def ensure_directories(project_root: Path) -> None:
    """Create required output directories if they do not exist."""
    (project_root / "data" / "processed").mkdir(parents=True, exist_ok=True)
    (project_root / "data" / "raw").mkdir(parents=True, exist_ok=True)
    (project_root / "logs").mkdir(parents=True, exist_ok=True)



def append_to_csv(df: pd.DataFrame, csv_path: Path) -> None:
    """Append DataFrame rows to a CSV file, writing the header only once."""
    file_exists = csv_path.exists()
    df.to_csv(csv_path, mode="a", header=not file_exists, index=False)



def append_to_sqlite(df: pd.DataFrame, db_path: Path, table_name: str = "weather_observations") -> None:
    """Append DataFrame rows to a SQLite database table."""
    with sqlite3.connect(db_path) as connection:
        df.to_sql(table_name, connection, if_exists="append", index=False)