# Generated by Django 4.2.2 on 2023-07-11 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmailAutomationBot', '0007_lastemaildatetime_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='file_data',
            field=models.FileField(upload_to=''),
        ),
    ]
