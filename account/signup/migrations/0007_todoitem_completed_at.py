# Generated by Django 4.2.11 on 2024-05-15 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0006_todoitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
