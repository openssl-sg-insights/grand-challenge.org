# Generated by Django 3.1.11 on 2021-06-20 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("algorithms", "0009_auto_20210601_0802"),
    ]

    operations = [
        migrations.AddField(
            model_name="algorithm",
            name="repo_name",
            field=models.CharField(blank=True, max_length=512),
        ),
    ]