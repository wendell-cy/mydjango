# Generated by Django 3.0.11 on 2021-01-07 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ('-is_accepted', '-created_at'), 'verbose_name': '答案', 'verbose_name_plural': '答案'},
        ),
    ]
