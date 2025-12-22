# Generated migration for adding post_file_ids, post_caption, and post_requested_at fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_add_post_file_ids_and_caption'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='student_submissions' AND column_name='post_file_ids') THEN
                    ALTER TABLE student_submissions ADD COLUMN post_file_ids TEXT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='student_submissions' AND column_name='post_caption') THEN
                    ALTER TABLE student_submissions ADD COLUMN post_caption TEXT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='student_submissions' AND column_name='post_requested_at') THEN
                    ALTER TABLE student_submissions ADD COLUMN post_requested_at TIMESTAMP NULL;
                END IF;
            END $$;
            """,
            reverse_sql="SELECT 1;"  # No-op for reverse
        ),
    ]
