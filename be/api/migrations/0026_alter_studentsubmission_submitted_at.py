# Generated migration to fix submitted_at field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_studentsubmission_is_late'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsubmission',
            name='submitted_at',
            field=models.DateTimeField(blank=True, null=True, help_text='Set when work is actually turned in, not when draft is created'),
        ),
    ]
