from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from coursesystem.models import * 
from . import populate

def is_student(user):
	return Student.objects.get(user=user)

def is_faculty(user):
	return Professor.objects.get(user=user)

def calc_letter_grade(grade):
	from math import ceil
	grades = 'ABCDFFFFFF'
	if grade > 0:
		return grades[10 - ceil(grade / 10)]
	else:
		return 'F'

def populate_data(request):
	if request.GET.get('populate') == 'students':
		populate.populate_students()
	if request.GET.get('populate') == 'professors':
		populate.populate_professors()
	if request.GET.get('populate') == 'departments':
		populate.update_dept_head()
	if request.GET.get('populate') == 'capstone':
		populate.update_capstone_sections()

	return render(request,'coursesystem/home.html')

def home(request):
	if request.user.is_authenticated:
		if is_student(request.user):
			return redirect('student/')
		elif is_faculty(request.user):
			return redirect('faculty/')
		elif request.user.is_superuser:
			return redirect('admin/')
	else:
		return redirect('login')

	return render(request,'coursesystem/home.html')

def signup(request):
	form = UserCreationForm
	successurl = reverse_lazy('login')
	return render(request, 'coursesystem/signup.html', {'form': form})

def student_home(request):
	if not is_student(request.user):
		return redirect('/')

	student_courses = Enrolls.objects.filter(student_email=request.user.username)
	for course in student_courses:
		teaching_team_id = course.course_section.prof_team.teaching_team_id
		prof_emails = [x.prof_email for x in Prof_team_members.objects.filter(teaching_team_id=teaching_team_id)]
		profs = [x for x in Professor.objects.filter(email__in=prof_emails)]
		course.profs = profs

		hws = [x for x in Homework_grades.objects.filter(student_email=request.user.username,course_section=course.course_section)]
		course.hws = hws

		exams = [x for x in Exam_grades.objects.filter(student_email=request.user.username,course_section=course.course_section)]
		course.exams = exams

		grades_hw = [x.hw_grade for x in hws]
		grades_exams = [x.exam_grade for x in exams]

		total_grade = 0
		if grades_hw:
			total_grade += sum(grades_hw) / len(grades_hw) * .5

		if grades_exams:
			total_grade += sum(grades_exams) / len(grades_exams) * .5

		letter_grade = calc_letter_grade(total_grade)
		course.grade = total_grade
		course.letter_grade = letter_grade
	context = {
		'enrolled': student_courses
	}

	return render(request,'coursesystem/student/home.html', context)

def faculty_home(request):
	if not is_faculty(request.user):
		return redirect('/')

	return render(request,'coursesystem/faculty/home.html')

def admin_home(request):
	if not request.user.is_superuser:
		return redirect('/')

	return render(request,'coursesystem/admin/home.html')