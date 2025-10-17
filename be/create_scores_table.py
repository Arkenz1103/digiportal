import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from django.db import connection

sql = """
CREATE TABLE IF NOT EXISTS submission_scores (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER NOT NULL UNIQUE REFERENCES student_submissions(id) ON DELETE CASCADE,
    creativity_score INTEGER DEFAULT 0,
    creativity_max INTEGER DEFAULT 10,
    technical_skill_score INTEGER DEFAULT 0,
    technical_skill_max INTEGER DEFAULT 10,
    requirements_score INTEGER DEFAULT 0,
    requirements_max INTEGER DEFAULT 10,
    total_score INTEGER DEFAULT 0,
    max_score INTEGER DEFAULT 30,
    scored_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    scored_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_submission_scores_submission_id ON submission_scores(submission_id);
CREATE INDEX IF NOT EXISTS idx_submission_scores_scored_by_id ON submission_scores(scored_by_id);
"""

with connection.cursor() as cursor:
    cursor.execute(sql)
    print("✅ submission_scores table created successfully!")
