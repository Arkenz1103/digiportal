# ✅ FINAL FIX - Create submission_scores Table

## What Happened
The migration tried to create `student_submissions` table which already exists, causing an error.

## Solution - Run This SQL

### **Step 1: Open pgAdmin or your PostgreSQL client**

### **Step 2: Copy and paste this SQL:**

```sql
-- Create submission_scores table
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

-- Add foreign keys
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

-- Verify it worked
SELECT 'Table created successfully!' as status;
```

### **Step 3: Verify it worked**

Run this to check:
```sql
SELECT * FROM submission_scores;
```

Should return empty result (no errors).

### **Step 4: Mark migration as applied**

In your terminal:
```bash
cd C:\Users\ACER\Downloads\digiportal\be
py manage.py migrate --fake
```

### **Step 5: Restart Django server**

```bash
py manage.py runserver
```

## Test the Scoring Feature

1. Go to **Teacher Outputs** page
2. Click **"Add Score"** on a submission
3. Enter scores (e.g., 10, 4, 4)
4. Click **"Confirm"**
5. ✅ Should work!

## If You Don't Have pgAdmin

### Option A: Use Django Shell

```bash
cd be
py manage.py shell
```

Then paste:
```python
from django.db import connection

sql = """
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
"""

with connection.cursor() as cursor:
    cursor.execute(sql)
    cursor.execute("ALTER TABLE submission_scores ADD CONSTRAINT fk_submission FOREIGN KEY (submission_id) REFERENCES student_submissions(id) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE submission_scores ADD CONSTRAINT fk_scored_by FOREIGN KEY (scored_by_id) REFERENCES users(id) ON DELETE SET NULL;")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_submission_scores_submission_id ON submission_scores(submission_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_submission_scores_scored_by_id ON submission_scores(scored_by_id);")

print("✅ Done!")
exit()
```

### Option B: Run the Python Script

```bash
cd be
py verify_table.py
```

This will check if the table exists and create it if needed.

## Summary

✅ **SQL provided** - Copy and run in PostgreSQL  
✅ **Migration marked as fake** - Won't try to create existing tables  
✅ **Django server ready** - Restart and test  
✅ **Scoring will work** - Table is ready!  

After running the SQL, the scoring feature will work perfectly! 🎉
