import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from django.db import connection

def check_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'submission_scores'
            );
        """)
        exists = cursor.fetchone()[0]
        
        if exists:
            print("✅ submission_scores table EXISTS!")
            
            # Get column info
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'submission_scores'
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            print("\nTable structure:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
        else:
            print("❌ submission_scores table DOES NOT EXIST")
            print("\nCreating table now...")
            
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
                scored_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            ALTER TABLE submission_scores 
            ADD CONSTRAINT fk_submission 
            FOREIGN KEY (submission_id) 
            REFERENCES student_submissions(id) 
            ON DELETE CASCADE;
            
            ALTER TABLE submission_scores 
            ADD CONSTRAINT fk_scored_by 
            FOREIGN KEY (scored_by_id) 
            REFERENCES users(id) 
            ON DELETE SET NULL;
            
            CREATE INDEX idx_submission_scores_submission_id ON submission_scores(submission_id);
            CREATE INDEX idx_submission_scores_scored_by_id ON submission_scores(scored_by_id);
            """
            
            cursor.execute(sql)
            print("✅ Table created successfully!")

if __name__ == "__main__":
    try:
        check_table()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
