# Generated by Django 2.2.12 on 2021-04-08 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='decommissioning_date',
            field=models.DateField(null=True),
        ),
    ]