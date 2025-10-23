# Migration to fix submitted_at for existing submissions

from django.db import migrations


def fix_submitted_at(apps, schema_editor):
    """
    For existing submissions that are not drafts,
    keep their current submitted_at as it represents when they were created.
    For drafts, set submitted_at to None (will be set when turned in).
    """
    StudentSubmission = apps.get_model('api', 'StudentSubmission')
    
    # Set submitted_at to None for all drafts
    drafts = StudentSubmission.objects.filter(status='draft')
    drafts.update(submitted_at=None)
    
    print(f"✅ Fixed {drafts.count()} draft submissions (set submitted_at to None)")
    
    # For non-draft submissions, submitted_at is already set (from creation time)
    # This is acceptable as it represents when they were submitted
    non_drafts = StudentSubmission.objects.exclude(status='draft')
    print(f"ℹ️  {non_drafts.count()} submitted works kept their submitted_at timestamps")


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_studentsubmission_submitted_at'),
    ]

    operations = [
        migrations.RunPython(fix_submitted_at, reverse_code=migrations.RunPython.noop),
    ]
