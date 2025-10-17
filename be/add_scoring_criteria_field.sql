-- Add scoring_criteria column to portfolio_activities table
-- This replaces the individual creativity_max, technical_max, requirements_max columns

-- Add the new JSON field
ALTER TABLE portfolio_activities 
ADD COLUMN IF NOT EXISTS scoring_criteria TEXT;

-- Drop old columns if they exist
ALTER TABLE portfolio_activities 
DROP COLUMN IF EXISTS creativity_max,
DROP COLUMN IF EXISTS technical_max,
DROP COLUMN IF EXISTS requirements_max;

-- Verify the change
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'portfolio_activities' 
AND column_name = 'scoring_criteria';

-- Example of what the JSON data looks like:
-- [{"name": "Creativity and originality", "maxScore": 10}, {"name": "Technical skill", "maxScore": 15}]
