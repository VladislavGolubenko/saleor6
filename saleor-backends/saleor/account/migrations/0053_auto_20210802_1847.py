# Generated by Django 3.1.2 on 2021-08-02 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0052_auto_20210730_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='addresses',
            new_name='addressess',
        ),
    ]
