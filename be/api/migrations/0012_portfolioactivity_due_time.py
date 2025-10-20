# Generated migration for adding due_time field to PortfolioActivity

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remarkreadstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolioactivity',
            name='due_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
