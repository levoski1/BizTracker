# Generated by Django 5.0.7 on 2024-08-11 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='description',
            new_name='text',
        ),
    ]