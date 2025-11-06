import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from django.db import connection

def add_classroom_column():
    """Add classroom_id column to newsfeed_posts table"""
    with connection.cursor() as cursor:
        try:
            # Check if column already exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='newsfeed_posts' AND column_name='classroom_id';
            """)
            
            if cursor.fetchone():
                print("✅ classroom_id column already exists in newsfeed_posts table")
                return
            
            # Add classroom_id column
            print("📝 Adding classroom_id column to newsfeed_posts table...")
            cursor.execute("""
                ALTER TABLE newsfeed_posts 
                ADD COLUMN classroom_id INTEGER REFERENCES classrooms(id) ON DELETE CASCADE;
            """)
            
            print("✅ Successfully added classroom_id column")
            
            # Update existing posts to set classroom from student
            print("📝 Updating existing posts with classroom data...")
            cursor.execute("""
                UPDATE newsfeed_posts 
                SET classroom_id = users.classroom_id 
                FROM users 
                WHERE newsfeed_posts.student_id = users.id 
                AND users.classroom_id IS NOT NULL;
            """)
            
            rows_updated = cursor.rowcount
            print(f"✅ Updated {rows_updated} existing posts with classroom data")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    print("🚀 Starting migration: Add classroom to newsfeed posts")
    add_classroom_column()
    print("✅ Migration complete!")
