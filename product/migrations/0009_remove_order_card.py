# Generated by Django 4.2.7 on 2024-04-20 10:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0008_order_card"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="card",
        ),
    ]
