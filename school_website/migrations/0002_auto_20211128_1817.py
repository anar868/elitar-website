# Generated by Django 3.1.4 on 2021-11-28 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='grade_number',
            field=models.IntegerField(),
        ),
    ]
