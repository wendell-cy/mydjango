# Generated by Django 3.0.11 on 2020-12-14 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201213_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='github',
            field=models.URLField(blank=True, default='', max_length=50, null=True, verbose_name='GitHub链接'),
        ),
    ]
