# Generated by Django 2.2.5 on 2020-01-12 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='calendar_url',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]
