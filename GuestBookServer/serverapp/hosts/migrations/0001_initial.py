# Generated by Django 3.0.4 on 2020-07-08 00:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(max_length=250, verbose_name='Event Title')),
                ('event_date', models.DateField(verbose_name='Event Date')),
                ('event_time', models.TimeField(default='12:00', verbose_name='Event Time')),
                ('unique_code', models.CharField(default='1aPwklekr', max_length=250, verbose_name='Unique Code')),
                ('num_vid_clips', models.IntegerField(default=0, verbose_name='Number of video clips')),
                ('max_num_vid_clips', models.IntegerField(default=100, verbose_name='Max number of video clips')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['event_date', 'event_time'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(default='vid.mp4', max_length=250, verbose_name='Event Title')),
                ('guest_name', models.CharField(default='anonymous', max_length=250, verbose_name='Guest Name')),
                ('thumbnailfpname', models.CharField(default='unknown', max_length=5000, verbose_name='Thumbnail Filename')),
                ('processedfpname', models.CharField(default='unknown', max_length=5000, verbose_name='Video Filename')),
                ('minifpname', models.CharField(default='unknown', max_length=5000, verbose_name='Mini Video Filename')),
                ('upload_date', models.DateField(default='20200101', verbose_name='Upload Date')),
                ('upload_time', models.TimeField(default='12:00', verbose_name='Upload Time')),
                ('event', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='hosts.Event')),
            ],
            options={
                'ordering': ['upload_date', 'upload_time'],
            },
        ),
    ]