# Generated by Django 2.0.5 on 2018-06-12 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("challenges", "0003_challenge_allow_unfiltered_page_html")]

    operations = [
        migrations.RenameField(
            model_name="challenge", old_name="logo", new_name="logo_path"
        )
    ]
