# Generated by Django 4.2.5 on 2023-12-28 12:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0015_alter_listing_end_time_alter_user_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 29, 12, 57, 4, 361606, tzinfo=datetime.timezone.utc)),
        ),
    ]