# Generated by Django 2.2.1 on 2019-05-11 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(related_name='categories', to='blog.Category'),
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(related_name='comments', to='blog.Category'),
        ),
    ]