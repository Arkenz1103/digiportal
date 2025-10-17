-- ============================================
-- CREATE SUBMISSION_SCORES TABLE
-- Run this in your PostgreSQL database
-- ============================================

-- Create the table
CREATE TABLE IF NOT EXISTS submission_scores (
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

-- Add foreign key constraints
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

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_submission_scores_submission_id ON submission_scores(submission_id);
CREATE INDEX IF NOT EXISTS idx_submission_scores_scored_by_id ON submission_scores(scored_by_id);

-- Verify table was created
SELECT 'Table created successfully!' as status;
SELECT * FROM submission_scores LIMIT 1;
