import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
print(f"Checking database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("\nExisting tables:")
for table in tables:
    print(f"  - {table[0]}")

# Check if portfolio_folders exists
if ('portfolio_folders',) in tables:
    print("\n✓ portfolio_folders table EXISTS")
    cursor.execute("SELECT COUNT(*) FROM portfolio_folders")
    count = cursor.fetchone()[0]
    print(f"  Records: {count}")
else:
    print("\n✗ portfolio_folders table DOES NOT EXIST")
    print("\nAttempting to apply migrations...")

conn.close()
