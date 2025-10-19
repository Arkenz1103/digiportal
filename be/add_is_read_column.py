import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from django.db import connection

# Add is_read column to remarks table
with connection.cursor() as cursor:
    try:
        # Check if column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='remarks' AND column_name='is_read';
        """)
        result = cursor.fetchone()
        
        if result:
            print("Column 'is_read' already exists in 'remarks' table")
        else:
            # Add the column
            cursor.execute("""
                ALTER TABLE remarks 
                ADD COLUMN is_read BOOLEAN DEFAULT FALSE;
            """)
            print("Successfully added 'is_read' column to 'remarks' table")
            
    except Exception as e:
        print(f"Error: {e}")
        # Try SQLite syntax if PostgreSQL fails
        try:
            cursor.execute("""
                ALTER TABLE remarks 
                ADD COLUMN is_read INTEGER DEFAULT 0;
            """)
            print("Successfully added 'is_read' column to 'remarks' table (SQLite)")
        except Exception as e2:
            print(f"SQLite error: {e2}")

print("\nVerifying column was added...")
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM remarks LIMIT 1;")
    columns = [col[0] for col in cursor.description]
    print(f"Columns in remarks table: {columns}")
    
    if 'is_read' in columns:
        print("✓ Column 'is_read' is present!")
    else:
        print("✗ Column 'is_read' is NOT present!")
