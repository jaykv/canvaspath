# Generated by Django 2.1.7 on 2019-04-23 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coursesystem', '0006_auto_20190422_1915'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='exams',
            unique_together={('course_section', 'exam_no')},
        ),
        migrations.AlterUniqueTogether(
            name='homework',
            unique_together={('course_section', 'hw_no')},
        ),
    ]
