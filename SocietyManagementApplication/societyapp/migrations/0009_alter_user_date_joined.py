# Generated by Django 4.0.3 on 2022-04-07 08:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('societyapp', '0008_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 8, 5, 44, 325552, tzinfo=utc)),
        ),
    ]
