# Generated by Django 4.1.7 on 2023-03-24 19:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_order_country_alter_order_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_no',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
