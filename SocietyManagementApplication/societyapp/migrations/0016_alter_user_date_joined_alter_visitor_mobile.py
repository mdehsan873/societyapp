# Generated by Django 4.0.3 on 2022-04-13 12:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('societyapp', '0015_visitor_gender_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 13, 12, 23, 53, 394827, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='mobile',
            field=models.TextField(),
        ),
    ]