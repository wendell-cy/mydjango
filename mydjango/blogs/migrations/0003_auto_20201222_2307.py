# Generated by Django 3.0.11 on 2020-12-22 15:07

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_article_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=mdeditor.fields.MDTextField(verbose_name='文章内容'),
        ),
    ]