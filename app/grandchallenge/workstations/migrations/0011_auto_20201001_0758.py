# Generated by Django 3.1.1 on 2020-10-01 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workstations", "0010_session_ping_times"),
    ]

    operations = [
        migrations.AlterField(
            model_name="session",
            name="ping_times",
            field=models.JSONField(default=None, null=True),
        ),
    ]
