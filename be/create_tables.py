import sqlite3
import os
#TRYING SOMETHING TO COMMIT
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
print(f"Connecting to database: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Create portfolio_folders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio_folders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    print("✓ Created/verified portfolio_folders table")
    
    # Create portfolio_activities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type VARCHAR(100) NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            due_date DATE,
            file_path VARCHAR(500),
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            folder_id INTEGER NOT NULL,
            FOREIGN KEY (folder_id) REFERENCES portfolio_folders (id) ON DELETE CASCADE
        )
    """)
    print("✓ Created/verified portfolio_activities table")
    
    # Mark the migration as applied
    cursor.execute("""
        INSERT OR IGNORE INTO django_migrations (app, name, applied)
        VALUES ('api', '0001_initial', datetime('now'))
    """)
    print("✓ Marked api.0001_initial migration as applied")
    
    conn.commit()
    print("\n✓✓✓ ALL TABLES CREATED SUCCESSFULLY ✓✓✓")
    
    # Verify tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%portfolio%'")
    tables = cursor.fetchall()
    print(f"\nVerification - Found {len(tables)} portfolio tables:")
    for table in tables:
        print(f"  - {table[0]}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    conn.rollback()
finally:
    conn.close()

print("\nDone! You can now restart the Django server.")
