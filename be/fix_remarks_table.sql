-- Add is_read column to remarks table if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='remarks' AND column_name='is_read'
    ) THEN
        ALTER TABLE remarks ADD COLUMN is_read BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Column is_read added successfully';
    ELSE
        RAISE NOTICE 'Column is_read already exists';
    END IF;
END $$;

-- Update all existing remarks to be unread
UPDATE remarks SET is_read = FALSE WHERE is_read IS NULL;

-- Verify the column exists
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'remarks' AND column_name = 'is_read';
