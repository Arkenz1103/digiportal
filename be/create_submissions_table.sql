-- Create student_submissions table
CREATE TABLE IF NOT EXISTS student_submissions (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    caption TEXT,
    file_path VARCHAR(500),
    file_type VARCHAR(50),
    score INTEGER,
    feedback TEXT,
    status VARCHAR(50) DEFAULT 'unscored',
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    scored_at TIMESTAMP,
    FOREIGN KEY (activity_id) REFERENCES portfolio_activities (id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_submissions_activity ON student_submissions(activity_id);
CREATE INDEX IF NOT EXISTS idx_submissions_student ON student_submissions(student_id);
CREATE INDEX IF NOT EXISTS idx_submissions_status ON student_submissions(status);
