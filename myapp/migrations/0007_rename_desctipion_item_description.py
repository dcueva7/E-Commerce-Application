# Generated by Django 4.1.7 on 2023-03-09 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_item_desctipion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='desctipion',
            new_name='description',
        ),
    ]
