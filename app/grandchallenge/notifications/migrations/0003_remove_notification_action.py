# Generated by Django 3.1.13 on 2021-09-10 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0002_auto_20210906_0855"),
    ]

    operations = [
        migrations.RemoveField(model_name="notification", name="action",),
    ]