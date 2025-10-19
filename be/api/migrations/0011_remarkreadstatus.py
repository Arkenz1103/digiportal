# Generated migration for RemarkReadStatus model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remark_is_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemarkReadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_at', models.DateTimeField(auto_now_add=True)),
                ('remark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_by', to='api.remark')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remarks_read', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'remark_read_status',
                'ordering': ['-read_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='remarkreadstatus',
            constraint=models.UniqueConstraint(fields=('remark', 'user'), name='unique_remark_user'),
        ),
    ]
