# Generated by Django 5.1.4 on 2024-12-19 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0003_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="list",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="lists.list",
            ),
        ),
    ]
