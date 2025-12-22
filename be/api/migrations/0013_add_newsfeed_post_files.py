# Generated migration for adding NewsfeedPostFile model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_add_post_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsfeedPostFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.TextField(blank=True, null=True)),
                ('file_type', models.CharField(default='image', max_length=50)),
                ('file_name', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='api.newsfeedpost')),
            ],
            options={
                'db_table': 'newsfeed_post_files',
                'ordering': ['order', 'created_at'],
            },
        ),
    ]
