# Generated migration for ActivityInstructionFile model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_add_newsfeed_post_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityInstructionFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='instruction_files/%Y/%m/%d/')),
                ('file_name', models.CharField(max_length=255)),
                ('file_type', models.CharField(blank=True, max_length=100, null=True)),
                ('file_size', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instruction_files', to='api.portfolioactivity')),
            ],
            options={
                'db_table': 'activity_instruction_files',
            },
        ),
    ]
