# Generated by Django 2.1.7 on 2019-04-23 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursesystem', '0009_auto_20190423_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam_grades',
            name='exam_no',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coursesystem.Exams'),
        ),
    ]
