from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.html import escape

from coursesystem.models import * 
from . import populate
import json

def is_student(user):
	return Student.objects.filter(user=user).exists()

def is_faculty(user):
	return Professor.objects.filter(user=user).exists()

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
	if request.GET.get('populate') == 'homework':
		populate.update_hw()
	if request.GET.get('populate') == 'exam':
		populate.update_exam()

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
	if not request.user.is_authenticated or not is_student(request.user):
		return redirect('/')

	student_courses = Enrolls.objects.filter(student_email=request.user.username)
	for course in student_courses:
		teaching_team_id = course.course_section.prof_team.teaching_team_id
		prof_emails = [x.prof_email for x in Prof_team_members.objects.filter(teaching_team_id=teaching_team_id)]
		profs = [x for x in Professor.objects.filter(email__in=prof_emails)]
		course.profs = profs

		hws = [x for x in Homework.objects.filter(course_section=course.course_section)]

		for hw in hws:
			try:
				hw.hw_grade = Homework_grades.objects.get(student_email=request.user.username,hw_no=hw).hw_grade
			except:
				hw.hw_grade = None
		course.hws = hws


		exams = [x for x in Exams.objects.filter(course_section=course.course_section)]
		for exam in exams:
			try:
				exam.exam_grade = Exam_grades.objects.get(student_email=request.user.username,exam_no=exam).exam_grade
			except:
				exam.exam_grade = None
		course.exams = exams

		grades_hw = [x.hw_grade for x in hws if x.hw_grade]
		grades_exams = [x.exam_grade for x in exams if x.exam_grade]

		total_grade = 0
		if grades_hw:
			total_grade += sum(grades_hw) / len(grades_hw) * .5

		if grades_exams:
			total_grade += sum(grades_exams) / len(grades_exams) * .5

		letter_grade = calc_letter_grade(total_grade)
		course.grade = total_grade
		course.letter_grade = letter_grade

	request.user.student = Student.objects.get(user=request.user)
	context = {
		'enrolled': student_courses
	}

	return render(request,'coursesystem/student/home.html', context)

def faculty_home(request):
	if not request.user.is_authenticated or not is_faculty(request.user):
		return redirect('/')

	prof_team_ids = [x.teaching_team_id for x in Prof_team_members.objects.filter(prof_email=request.user.username)]
	if prof_team_ids:
		prof_courses = Sections.objects.filter(prof_team__in=prof_team_ids)
		for section in prof_courses:
			teaching_team_id = section.prof_team.teaching_team_id
			prof_emails = [x.prof_email for x in Prof_team_members.objects.filter(teaching_team_id=teaching_team_id)]
			profs = [x for x in Professor.objects.filter(email__in=prof_emails)]
			section.profs = profs
			
			hws = [x for x in Homework.objects.filter(course_section=section)]
			section.hws = hws

			exams = [x for x in Exams.objects.filter(course_section=section)]
			section.exams = exams
			
			student_emails = [x.student_email for x in Enrolls.objects.filter(course_section=section)]
			students = [x for x in Student.objects.filter(email__in=student_emails)]
			for student in students:
				student_hws = Homework_grades.objects.filter(course_section = section, student_email=student.email)
				student_exams = Exam_grades.objects.filter(course_section = section, student_email=student.email) 
				student.hw = {}
				for student_hw in student_hws:
					student.hw[student_hw.hw_no.id] = student_hw.hw_grade
				student.exam = {}
				for student_exam in student_exams:
					student.exam[student_exam.exam_no.id] = student_exam.exam_grade
			section.students = students
			section.grade = '80'
			section.letter_grade = 'A'

		request.user.professor = Professor.objects.get(user=request.user)
		context = {
			'teaching': prof_courses
		}
	return render(request,'coursesystem/faculty/home.html', context)

def admin_home(request):
	if not request.user.is_authenticated or not request.user.is_superuser:
		return redirect('/')

	return render(request,'coursesystem/admin/home.html')

def add_assignment(request):
	try:
		list_data = json.loads(request.GET.get('data'))
		form_data = {x['name']:x['value'] for x in list_data}

		section = int(float(form_data['section']))
		assignment_no = int(float(form_data['assignment_no']))
		assignment_details = escape(form_data['assignment_details'])
		assignment_type = escape(form_data['assignment_type'])

		course_section = Sections.objects.get(pk=section)
		if assignment_type == 'Homework':
			new_hw = Homework(course_section=course_section, hw_details=assignment_details, hw_no=assignment_no)
			new_hw.save()
		elif assignment_type == 'Exam':
			new_exam = Exams(course_section=course_section, exam_details=assignment_details, exam_no=assignment_no)
			new_exam.save()
		else:
			data = {'success': False}
			pass

		data = {'success': True}
	except Exception as e:
		print(e)
		data = {'success': False}

	return JsonResponse(data)

def update_grades(request):
	try:
		list_data = json.loads(request.GET.get('data'))
		form_data = {x['name']:x['value'] for x in list_data}

		section = int(float(form_data['section']))
		assignment_type = form_data['assignment_type']
		assignment_id = int(float(form_data['assignment_no']))

		for x in ['assignment_type', 'section', 'assignment_no']:
			form_data.pop(x)

		course_section = Sections.objects.get(pk=section)
		if assignment_type == 'Homework':
			hw_no = Homework.objects.get(pk=assignment_id)
			for email, grade in form_data.items():
				student_email = escape(email)
				if not student_email:
					continue

				try:
					hw_grade = float(grade)
				except:
					Homework_grades.objects.filter(course_section=course_section, hw_no=hw_no, student_email=student_email).delete()
					continue

				obj, created = Homework_grades.objects.update_or_create(
						course_section=course_section, hw_no=hw_no, student_email=student_email, 
						defaults = {'hw_grade': hw_grade}
					)
		elif assignment_type == 'Exam':
			exam_no = Exams.objects.get(pk=assignment_id)
			for email, grade in form_data.items():
				student_email = escape(email)

				if not student_email:
					continue

				try:
					exam_grade = float(grade)
				except:
					Exam_grades.objects.filter(course_section=course_section, exam_no=exam_no, student_email=student_email).delete()
					continue

				obj, created = Exam_grades.objects.update_or_create(
						course_section=course_section, exam_no=exam_no, student_email=student_email, 
						defaults = {'exam_grade': exam_grade}
					)

		data = {'success':True}
	except Exception as e:
		print(e)
		data = {'success':False}
		pass
	return JsonResponse(data)
def delete_exam(request):
	examid = request.GET.get('exam_id')
	try:
		Exams.objects.get(pk=examid).delete()
		data = {'success': True}
	except:
		data = {'success': False}
	return JsonResponse(data)

def delete_hw(request):
	hwid = request.GET.get('hw_id')
	try:
		Homework.objects.get(pk=hwid).delete()
		data = {'success': True}
	except:
		data = {'success': False}
	return JsonResponse(data)