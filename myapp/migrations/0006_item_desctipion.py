# Generated by Django 4.1.7 on 2023-03-09 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_item_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='desctipion',
            field=models.TextField(default="this is a test dessctiption for any item that is craeted without entering a description.  this shouldn't ever happen if I am creating the item from the admin menu but it might happen if I create the item through the SQL shell available with django"),
            preserve_default=False,
        ),
    ]