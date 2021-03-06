# Generated by Django 3.2.1 on 2021-05-12 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('butlercfg', '0007_auto_20210512_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(blank=True, max_length=200, verbose_name='Модель')),
                ('caption', models.CharField(max_length=200, verbose_name='Номенклатура')),
                ('count', models.PositiveIntegerField(blank=True, verbose_name='Кол-во вх/вых')),
                ('price', models.IntegerField(blank=True, verbose_name='Цена')),
                ('level', models.ManyToManyField(to='butlercfg.Levels', verbose_name='Уровень')),
                ('system', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='butlercfg.systems', verbose_name='Подсистема')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='butlercfg.vendors', verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Устройство',
                'verbose_name_plural': 'Оборудование',
            },
        ),
    ]
