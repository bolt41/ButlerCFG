# Generated by Django 3.2.1 on 2021-05-11 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butlercfg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='systems',
            name='is_visible',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
