# Generated by Django 3.2.6 on 2021-12-12 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='image',
            field=models.ImageField(upload_to='uploads'),
        ),
    ]
