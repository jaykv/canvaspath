# Generated by Django 2.1.7 on 2019-04-23 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursesystem', '0008_auto_20190423_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework_grades',
            name='hw_no',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coursesystem.Homework'),
        ),
    ]
