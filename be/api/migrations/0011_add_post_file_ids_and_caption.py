# Generated migration for adding post_file_ids, post_caption, and post_requested_at fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_add_submission_file_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsubmission',
            name='post_file_ids',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentsubmission',
            name='post_caption',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentsubmission',
            name='post_requested_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
