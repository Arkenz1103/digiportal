import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from django.db import connection

def table_exists(table_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

def create_submission_scores_table():
    sql = """
    CREATE TABLE submission_scores (
        id SERIAL PRIMARY KEY,
        submission_id INTEGER NOT NULL UNIQUE,
        creativity_score INTEGER DEFAULT 0,
        creativity_max INTEGER DEFAULT 10,
        technical_skill_score INTEGER DEFAULT 0,
        technical_skill_max INTEGER DEFAULT 10,
        requirements_score INTEGER DEFAULT 0,
        requirements_max INTEGER DEFAULT 10,
        total_score INTEGER DEFAULT 0,
        max_score INTEGER DEFAULT 30,
        scored_by_id INTEGER,
        scored_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_submission FOREIGN KEY (submission_id) REFERENCES student_submissions(id) ON DELETE CASCADE,
        CONSTRAINT fk_scored_by FOREIGN KEY (scored_by_id) REFERENCES users(id) ON DELETE SET NULL
    );
    
    CREATE INDEX idx_submission_scores_submission_id ON submission_scores(submission_id);
    CREATE INDEX idx_submission_scores_scored_by_id ON submission_scores(scored_by_id);
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        print("✅ submission_scores table created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False

if __name__ == "__main__":
    print("Checking if submission_scores table exists...")
    
    if table_exists('submission_scores'):
        print("✅ Table already exists!")
    else:
        print("❌ Table does not exist. Creating...")
        create_submission_scores_table()
