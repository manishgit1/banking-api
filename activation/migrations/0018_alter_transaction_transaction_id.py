# Generated by Django 5.0.2 on 2024-03-05 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activation', '0017_alter_appuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
