# Generated by Django 4.0.6 on 2023-05-26 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
