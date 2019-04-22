# Generated by Django 2.1.7 on 2019-04-22 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursesystem', '0003_auto_20190422_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='dept_id',
            field=models.TextField(default=None, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='department',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='department',
            name='id',
        ),
    ]