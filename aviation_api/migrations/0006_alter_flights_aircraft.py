# Generated by Django 4.2.3 on 2023-07-11 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aviation_api', '0005_alter_flights_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flights',
            name='aircraft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='aviation_api.aircraft'),
        ),
    ]
