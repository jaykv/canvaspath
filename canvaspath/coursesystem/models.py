from django.db import models
from django.contrib.auth.models import User

class Zipcode(models.Model):
	zipcode = models.IntegerField(primary_key=True)
	city = models.TextField()
	state =  models.TextField()

class Student(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	email = models.EmailField(max_length=70)
	name = models.TextField()
	age = models.IntegerField()
	gender = models.CharField(max_length=1)
	major = models.TextField()
	street = models.TextField()
	zipcode = models.ForeignKey(Zipcode, on_delete=None)

	class Meta:
		unique_together = (('user', 'email'),)


class Department(models.Model):
	dept_id = models.TextField(primary_key=True)
	dept_name = models.TextField()
	dept_head = models.TextField()

class Professor(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	email = models.EmailField(max_length=70)
	name = models.TextField()
	age = models.IntegerField()
	gender = models.CharField(max_length=1)
	office_address = models.TextField()
	department = models.ForeignKey(Department, on_delete=None)
	title = models.TextField()

	class Meta:
		unique_together = (('user', 'email'),)


class Course(models.Model):
	course_id = models.TextField(primary_key=True)
	course_name = models.TextField()
	course_description = models.TextField()

class Prof_teams(models.Model):
	teaching_team_id = models.IntegerField(primary_key=True)

class Prof_team_members(models.Model):
	prof_email = models.TextField()
	teaching_team_id = models.ForeignKey(Prof_teams, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('prof_email', 'teaching_team_id'),)

class Sections(models.Model):
	course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
	sec_no = models.IntegerField()
	section_type = models.TextField()
	limit = models.IntegerField()
	prof_team = models.ForeignKey(Prof_teams, on_delete=None, null=True)

	class Meta:
		unique_together = (('course_id', 'sec_no'),)

class Enrolls(models.Model):
	student_email = models.TextField()
	course_section = models.ForeignKey(Sections, on_delete=models.CASCADE)

class Homework(models.Model):
	course_section = models.ForeignKey(Sections, on_delete=models.CASCADE)
	hw_no = models.IntegerField()
	hw_details = models.TextField()

class Homework_grades(models.Model):
	student_email = models.TextField()
	course_section = models.ForeignKey(Sections, on_delete=models.CASCADE)
	hw_no = models.ForeignKey(Homework, on_delete=models.CASCADE)
	hw_grade = models.FloatField()

class Exams(models.Model):
	course_section = models.ForeignKey(Sections, on_delete=models.CASCADE)
	exam_no = models.IntegerField()
	exam_details = models.TextField()

class Exam_grades(models.Model):
	student_email = models.TextField()
	course_section = models.ForeignKey(Sections, on_delete=models.CASCADE)
	exam_no = models.ForeignKey(Exams, on_delete=models.CASCADE)
	exam_grade = models.FloatField()

class Capstone_section(models.Model):
	course_section = models.ForeignKey(Sections, on_delete=models.CASCADE)
	project_no = models.IntegerField()
	sponsor_id = models.EmailField(null=True)

	class Meta:
		unique_together = (('course_section', 'project_no'),)
		
class Capstone_Team(models.Model):
	course_section = models.ForeignKey(Sections, on_delete=models.CASCADE)
	capstone_team_id = models.IntegerField()
	project_no = models.IntegerField()

class Capstone_Team_Members(models.Model):
	student_email = models.EmailField(max_length=70)
	capstone_team_id = models.ForeignKey(Capstone_Team, on_delete=models.CASCADE)
	course_section = models.ForeignKey(Sections, on_delete=models.CASCADE)

class Capstone_grades(models.Model):
	capstone_team_id = models.ForeignKey(Capstone_Team, on_delete=models.CASCADE)
	capstone_grade = models.FloatField()
