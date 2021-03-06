# Generated by Django 2.1.7 on 2019-04-22 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Capstone_grades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capstone_grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Capstone_section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_no', models.IntegerField()),
                ('sponsor_id', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Capstone_Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capstone_team_id', models.IntegerField()),
                ('project_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Capstone_Team_Members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_email', models.EmailField(max_length=70)),
                ('capstone_team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Capstone_Team')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.TextField(primary_key=True, serialize=False)),
                ('course_name', models.TextField()),
                ('course_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('dept_id', models.TextField(primary_key=True, serialize=False)),
                ('dept_name', models.TextField()),
                ('dept_head', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Enrolls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_email', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Exam_grades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_email', models.TextField()),
                ('exam_no', models.IntegerField()),
                ('exam_grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Exams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_no', models.IntegerField()),
                ('exam_details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hw_no', models.IntegerField()),
                ('hw_details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Homework_grades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_email', models.TextField()),
                ('hw_grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Prof_team_members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prof_email', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Prof_teams',
            fields=[
                ('teaching_team_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=70)),
                ('name', models.TextField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=1)),
                ('office_address', models.TextField()),
                ('title', models.TextField()),
                ('department', models.ForeignKey(on_delete=None, to='coursesystem.Department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sec_no', models.IntegerField()),
                ('section_type', models.TextField()),
                ('limit', models.IntegerField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Course')),
                ('prof_team', models.ForeignKey(on_delete=None, to='coursesystem.Prof_teams')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=70)),
                ('name', models.TextField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=1)),
                ('major', models.TextField()),
                ('street', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('zipcode', models.IntegerField(primary_key=True, serialize=False)),
                ('city', models.TextField()),
                ('state', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='zipcode',
            field=models.ForeignKey(on_delete=None, to='coursesystem.Zipcode'),
        ),
        migrations.AddField(
            model_name='prof_team_members',
            name='teaching_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Prof_teams'),
        ),
        migrations.AddField(
            model_name='homework_grades',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Sections'),
        ),
        migrations.AddField(
            model_name='homework_grades',
            name='hw_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Homework'),
        ),
        migrations.AddField(
            model_name='homework',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Sections'),
        ),
        migrations.AddField(
            model_name='exams',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Sections'),
        ),
        migrations.AddField(
            model_name='exam_grades',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Sections'),
        ),
        migrations.AddField(
            model_name='enrolls',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Sections'),
        ),
        migrations.AddField(
            model_name='capstone_team_members',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Sections'),
        ),
        migrations.AddField(
            model_name='capstone_team',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Sections'),
        ),
        migrations.AddField(
            model_name='capstone_section',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Sections'),
        ),
        migrations.AddField(
            model_name='capstone_grades',
            name='capstone_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursesystem.Capstone_Team'),
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('user', 'email')},
        ),
        migrations.AlterUniqueTogether(
            name='sections',
            unique_together={('course_id', 'sec_no')},
        ),
        migrations.AlterUniqueTogether(
            name='professor',
            unique_together={('user', 'email')},
        ),
        migrations.AlterUniqueTogether(
            name='prof_team_members',
            unique_together={('prof_email', 'teaching_team_id')},
        ),
        migrations.AlterUniqueTogether(
            name='homework_grades',
            unique_together={('course_section', 'student_email', 'hw_no')},
        ),
        migrations.AlterUniqueTogether(
            name='exams',
            unique_together={('course_section', 'exam_no')},
        ),
        migrations.AlterUniqueTogether(
            name='exam_grades',
            unique_together={('course_section', 'student_email', 'exam_no')},
        ),
        migrations.AlterUniqueTogether(
            name='capstone_team_members',
            unique_together={('course_section', 'student_email', 'capstone_team_id')},
        ),
        migrations.AlterUniqueTogether(
            name='capstone_team',
            unique_together={('course_section', 'capstone_team_id')},
        ),
        migrations.AlterUniqueTogether(
            name='capstone_section',
            unique_together={('course_section', 'project_no')},
        ),
    ]
