# Generated by Django 5.1.2 on 2024-11-16 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_portal', '0016_alter_community_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='comment',
            field=models.TextField(help_text='Enter your comment here.'),
        ),
    ]