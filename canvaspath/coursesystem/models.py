from django.db import models
from django.contrib.auth.models import User

class Zipcode(models.Model):
	zipcode = models.IntegerField(primary_key=True)
	city = models.TextField()
	state =  models.TextField()

class Student(models.Model):
	email = models.EmailField(max_length=70)
	name = models.TextField()
	age = models.IntegerField()
	gender = models.CharField(max_length=1)
	major = models.TextField()
	street = models.TextField()
	zipcode = models.ForeignKey(Zipcode)

class Department(models.Model):
	dept_name = models.TextField()
	dept_head = models.ForeignKey(Professor)

class Professor(models.Model):
	email = models.EmailField(max_length=70)
	name = models.TextField()
	age = models.IntegerField()
	gender = models.CharField(max_length=1)
	office_address = models.TextField()
	department = models.ForeignKey(Department)
	title = models.TextField()

class Course(models.Model):
	course_id = models.IntegerField(primary_key=True)
	course_name = models.TextField()
	course_description = models.TextField()

class Sections(models.Model):
	course_id = models.ForeignKey(Course, primary_key=True)
	sec_no = models.IntegerField(primary_key = True)
	section_type = models.TextField()
	limit = models.IntegerField()
	prof_team = models.ForeignKey(Prof_teams)

class Enrolls(models.Model):
	student_email = models.TextField()
	course_id = models.ForeignKey(Course)
	section_no = models.ForeignKey(Sections)

class Prof_teams(models.Model):
	team_id = models.IntegerField(primary_key=True)

class Prof_team_members(models.Model):
	prof_email = models.TextField()
	team_id = models.ForeignKey(Prof_teams)

class Homework(models.Model):
	course_id = models.ForeignKey(Course)
	sec_no = models.ForeignKey(Sections)
	hw_no = models.IntegerField()
	hw_details = models.TextField()

class Homework_grades(models.Model):
	student_email = models.TextField()
	course_id = models.ForeignKey(Course)
	sec_no = models.ForeignKey(Sections)
	hw_no = models.ForeignKey(Homework)
	grade = models.IntegerField()

class Exams(models.Model):
	course_id = models.ForeignKey(Course)
	sec_no = models.ForeignKey(Sections)
	exam_no = models.IntegerField()
	exam_details = models.TextField()

class Exam_grades(models.Model):
	student_email = models.TextField()
	course_id = models.ForeignKey(Course)
	sec_no = models.ForeignKey(Sections)
	exam_no = models.IntegerField()
	grade = models.IntegerField()

class Capstone_section(models.Model):
	course_id = models.ForeignKey(Course)
	sec_no = models.ForeignKey(Sections)
	project_no = models.IntegerField()
	sponsor_id = models.EmailField()
