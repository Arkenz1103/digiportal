# Migration to set reasonable submitted_at timestamps for existing submissions

from django.db import migrations
from django.utils import timezone


def set_reasonable_timestamps(apps, schema_editor):
    """
    For existing non-draft submissions without submitted_at,
    set it to current time as a reasonable default.
    This allows the timestamp to display while being accurate going forward.
    """
    StudentSubmission = apps.get_model('api', 'StudentSubmission')
    
    # Get non-draft submissions without submitted_at
    submissions_without_time = StudentSubmission.objects.filter(
        submitted_at__isnull=True
    ).exclude(status='draft')
    
    count = submissions_without_time.count()
    
    if count > 0:
        # Set to current time (Philippine Time)
        now = timezone.now()
        submissions_without_time.update(submitted_at=now)
        
        print(f"✅ Set submitted_at for {count} existing submissions to current time: {now}")
        print(f"ℹ️  These submissions will now display a timestamp")
    else:
        print(f"ℹ️  No submissions need timestamp updates")


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_alter_studentsubmission_status_and_more'),
    ]

    operations = [
        migrations.RunPython(set_reasonable_timestamps, reverse_code=migrations.RunPython.noop),
    ]
