# Generated migration to add criteria_scores field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_portfolioactivity_scoring_criteria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsubmission',
            name='criteria_scores',
            field=models.TextField(null=True, blank=True),
        ),
    ]
