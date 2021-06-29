# Generated by Django 3.2.1 on 2021-06-24 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PartitionSurv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('is_use', models.BooleanField(verbose_name='Использовать в опросах')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SystemSurv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('is_use', models.BooleanField(verbose_name='Использовать в опросах')),
            ],
            options={
                'verbose_name': 'Подсистема',
                'verbose_name_plural': 'Подсистемы',
                'ordering': ['name'],
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='QuestionSurv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=600, verbose_name='Текст')),
                ('is_use', models.BooleanField(verbose_name='Использовать в опросах')),
                ('partition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='butlersurv.partitionsurv', verbose_name='Связаный раздел')),
            ],
            options={
                'verbose_name': 'Подпись',
                'verbose_name_plural': 'Подписи',
            },
        ),
        migrations.AddField(
            model_name='partitionsurv',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='butlersurv.systemsurv', verbose_name='Подсистема'),
        ),
        migrations.CreateModel(
            name='AnswerSurv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(max_length=600, verbose_name='Вариант выбора')),
                ('is_use', models.BooleanField(verbose_name='Использовать в опросах')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='butlersurv.questionsurv', verbose_name='Связаный вопрос')),
            ],
            options={
                'verbose_name': 'Вариант выбора',
                'verbose_name_plural': 'Варианты выбора',
            },
        ),
        migrations.AlterUniqueTogether(
            name='partitionsurv',
            unique_together={('name',)},
        ),
    ]
