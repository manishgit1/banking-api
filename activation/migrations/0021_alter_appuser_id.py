# Generated by Django 5.0.2 on 2024-03-05 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activation', '0020_alter_appuser_id_alter_transaction_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
