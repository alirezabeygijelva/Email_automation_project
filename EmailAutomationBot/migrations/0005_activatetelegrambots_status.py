# Generated by Django 4.2.2 on 2023-08-14 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmailAutomationBot', '0004_rename_name_botgroupemailuserrelations_server_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activatetelegrambots',
            name='status',
            field=models.CharField(choices=[('Active', 'active'), ('Deactive', 'deactive')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
