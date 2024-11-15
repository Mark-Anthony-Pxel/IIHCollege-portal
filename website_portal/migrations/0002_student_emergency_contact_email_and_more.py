# Generated by Django 5.1.2 on 2024-10-26 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='emergency_contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='emergency_contact_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='emergency_contact_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='emergency_contact_relationship',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
