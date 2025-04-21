import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL", "sqlite:///exercise.db")

db_path = db_url.replace("sqlite:///", "")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS project_software_associations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    software_id INTEGER NOT NULL,
    UNIQUE(project_id, software_id),
    FOREIGN KEY(project_id) REFERENCES projects(id),
    FOREIGN KEY(software_id) REFERENCES software(id)
);
""")

conn.commit()
conn.close()
print("Migration complete.")
