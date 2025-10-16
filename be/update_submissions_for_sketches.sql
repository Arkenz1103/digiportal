-- Update student_submissions table to allow null activity_id for sketch submissions
-- This allows students to post sketches directly to newsfeed without an activity

-- Make activity_id nullable
ALTER TABLE student_submissions 
ALTER COLUMN activity_id DROP NOT NULL;

-- Drop the unique constraint if it exists
ALTER TABLE student_submissions 
DROP CONSTRAINT IF EXISTS student_submissions_activity_id_student_id_key;

-- Add comment
COMMENT ON COLUMN student_submissions.activity_id IS 'Activity ID - NULL for sketch pad submissions';
