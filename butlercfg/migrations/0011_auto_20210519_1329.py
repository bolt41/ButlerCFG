# Generated by Django 3.2.1 on 2021-05-19 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butlercfg', '0010_auto_20210517_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='systems',
            name='public_text',
            field=models.CharField(blank=True, max_length=300, verbose_name='В печатной форме'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='count',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Кол-во вх/вых'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='is_main',
            field=models.BooleanField(default=False, verbose_name='Базовый элемент подсистемы'),
        ),
    ]