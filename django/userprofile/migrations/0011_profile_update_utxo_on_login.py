# Generated by Django 3.2.20 on 2024-02-05 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0010_auto_20240205_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='update_utxo_on_login',
            field=models.BooleanField(default=True),
        ),
    ]