# Generated by Django 3.2.20 on 2023-08-12 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mempool_endpoint',
            field=models.CharField(blank=True, default='https://mempool.space', max_length=160),
        ),
    ]
