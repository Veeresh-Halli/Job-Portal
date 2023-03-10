# Generated by Django 4.1.7 on 2023-02-22 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobportalapp', '0002_joblisting'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=250, null=True)),
                ('file', models.FileField(upload_to='')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportalapp.joblisting')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
