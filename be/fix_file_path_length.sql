-- Increase file_path column length to handle data URLs
ALTER TABLE student_submissions 
ALTER COLUMN file_path TYPE TEXT;
