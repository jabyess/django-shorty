# Generated by Django 2.2.7 on 2019-11-08 18:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_auto_20191108_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
