# Generated by Django 4.1.7 on 2023-03-12 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_orderitem_ordered_orderitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
    ]
