# Generated by Django 4.2.11 on 2024-04-06 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("order_management", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderlineitems",
            name="user_id",
        ),
        migrations.AddField(
            model_name="orderlineitems",
            name="order_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="order_management.order",
            ),
            preserve_default=False,
        ),
    ]
