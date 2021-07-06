# Generated by Django 3.2.1 on 2021-05-11 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('butlercfg', '0004_alter_systems_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Params',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название параметра')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='butlercfg.systems', verbose_name='Подсистема')),
            ],
            options={
                'verbose_name': 'Параметр',
                'verbose_name_plural': 'Параметры',
                'ordering': ['name'],
                'unique_together': {('name',)},
            },
        ),
    ]