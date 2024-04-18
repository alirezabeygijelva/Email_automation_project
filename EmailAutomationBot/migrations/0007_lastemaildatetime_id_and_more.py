# Generated by Django 4.2.2 on 2023-07-11 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EmailAutomationBot', '0006_remove_lastemaildatetime_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lastemaildatetime',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lastemaildatetime',
            name='email_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmailAutomationBot.email'),
        ),
    ]
