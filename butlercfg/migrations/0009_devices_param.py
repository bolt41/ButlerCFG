# Generated by Django 3.2.1 on 2021-05-17 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('butlercfg', '0008_devices'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='param',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='butlercfg.params'),
        ),
    ]