-- Add post_to_feed column to student_submissions table
ALTER TABLE student_submissions 
ADD COLUMN IF NOT EXISTS post_to_feed BOOLEAN DEFAULT FALSE;

-- Add approval_status column for teacher approval
ALTER TABLE student_submissions 
ADD COLUMN IF NOT EXISTS approval_status VARCHAR(50) DEFAULT 'pending';

-- approval_status values: 'pending', 'approved', 'rejected'
