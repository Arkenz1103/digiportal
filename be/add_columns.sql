-- Add activity_type and due_date columns to portfolio_activities table
ALTER TABLE portfolio_activities 
ADD COLUMN IF NOT EXISTS activity_type VARCHAR(100) DEFAULT 'Quiz' NOT NULL;

ALTER TABLE portfolio_activities 
ADD COLUMN IF NOT EXISTS due_date DATE;

-- Add class_name column to portfolio_folders table
ALTER TABLE portfolio_folders 
ADD COLUMN IF NOT EXISTS class_name VARCHAR(255) DEFAULT 'General' NOT NULL;
