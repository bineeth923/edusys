# Generated by Django 3.0.7 on 2020-06-17 19:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('attendance', '0002_auto_20200618_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='division',
            field=models.CharField(max_length=20),
        ),
    ]
