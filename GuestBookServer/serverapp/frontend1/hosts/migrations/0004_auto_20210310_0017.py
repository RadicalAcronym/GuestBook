# Generated by Django 3.1.5 on 2021-03-10 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0003_video_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['position', 'upload_date', 'upload_time']},
        ),
    ]