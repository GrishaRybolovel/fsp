# Generated by Django 4.2.1 on 2023-05-26 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_user_role"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Message",
        ),
    ]
