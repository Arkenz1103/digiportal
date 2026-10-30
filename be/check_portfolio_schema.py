import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
print(f"Checking database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check portfolio_folders schema
cursor.execute("PRAGMA table_info(portfolio_folders);")
columns = cursor.fetchall()

print("\nportfolio_folders table schema:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

conn.close()
