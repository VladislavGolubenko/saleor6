# Generated by Django 2.2.6 on 2019-11-18 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("order", "0076_auto_20191018_0554")]

    operations = [
        migrations.RenameField(
            model_name="fulfillment", old_name="shipping_date", new_name="created"
        ),
        migrations.AlterField(
            model_name="fulfillment",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
