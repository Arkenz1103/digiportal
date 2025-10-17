# 🔧 Fix Scoring Error - Create Missing Table

## Error
```
relation "submission_scores" does not exist
```

## Solution

The `submission_scores` table needs to be created in your database.

### **Option 1: Run SQL File (Easiest)** ⭐

1. **Open your PostgreSQL client** (pgAdmin, DBeaver, or command line)

2. **Connect to your database**

3. **Run the SQL file:**
   - File location: `C:\Users\ACER\Downloads\digiportal\RUN_THIS_SQL.sql`
   - Or copy and paste this SQL:

```sql
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

CREATE INDEX IF NOT EXISTS idx_submission_scores_submission_id ON submission_scores(submission_id);
CREATE INDEX IF NOT EXISTS idx_submission_scores_scored_by_id ON submission_scores(scored_by_id);
```

4. **Verify it worked:**
```sql
SELECT * FROM submission_scores;
```

### **Option 2: Using psql Command Line**

```bash
cd C:\Users\ACER\Downloads\digiportal
psql -U your_username -d your_database -f RUN_THIS_SQL.sql
```

### **Option 3: Django Shell**

```bash
cd be
python manage.py shell
```

Then paste:
```python
from django.db import connection

sql = """
CREATE TABLE submission_scores (
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
    
print("✅ Table created!")
```

## After Creating the Table

1. **Restart Django server:**
```bash
cd be
py manage.py runserver
```

2. **Try scoring again:**
   - Go to Teacher Outputs
   - Click "Add Score"
   - Enter scores
   - Click "Confirm"
   - ✅ Should work now!

## Verify It's Working

Check the database:
```sql
-- Should show the new table structure
\d submission_scores

-- Should be empty initially
SELECT * FROM submission_scores;
```

After scoring a submission:
```sql
-- Should show the scored submission
SELECT * FROM submission_scores;
```

## What This Table Does

Stores detailed scoring criteria for each submission:
- **creativity_score** - Score for creativity (0-10)
- **technical_skill_score** - Score for technical skill (0-10)
- **requirements_score** - Score for requirements (0-10)
- **total_score** - Sum of all scores (0-30)
- **scored_by_id** - Which teacher scored it
- **scored_at** - When it was scored

## Troubleshooting

### If you get "permission denied"
Make sure you're connected as a user with CREATE TABLE permissions.

### If you get "already exists"
The table is already there! Just try scoring again.

### If you get "relation student_submissions does not exist"
You need to create the student_submissions table first. Check your database setup.

## Summary

✅ **SQL file created:** `RUN_THIS_SQL.sql`  
✅ **Run the SQL** in your PostgreSQL database  
✅ **Restart Django server**  
✅ **Try scoring again**  

The scoring feature will work after creating this table! 🎉
