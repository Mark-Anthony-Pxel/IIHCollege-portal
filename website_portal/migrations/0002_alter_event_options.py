# Generated by Django 5.1.2 on 2024-11-18 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-created_at'], 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
    ]
