-- Add scoring criteria columns to portfolio_activities table

ALTER TABLE portfolio_activities 
ADD COLUMN IF NOT EXISTS creativity_max INTEGER DEFAULT 10;

ALTER TABLE portfolio_activities 
ADD COLUMN IF NOT EXISTS technical_max INTEGER DEFAULT 10;

ALTER TABLE portfolio_activities 
ADD COLUMN IF NOT EXISTS requirements_max INTEGER DEFAULT 10;

-- Verify columns were added
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'portfolio_activities' 
AND column_name IN ('creativity_max', 'technical_max', 'requirements_max');
