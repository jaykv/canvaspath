from django.contrib.auth.models import User
from django.conf import settings
from coursesystem.models import * 
from django.contrib.auth.hashers import make_password
import os, csv

def update_capstone_sections():
	sections = Sections.objects.filter(section_type='Cap')
	for section in sections:
		prof_team = section.prof_team
		prof_members = Prof_team_members.objects.get(teaching_team_id=prof_team)
		sponsor_id = prof_members.prof_email

		new_cap_section = Capstone_section(course_section=section, project_no=1, sponsor_id=sponsor_id)
		new_cap_section.save()

		new_cap_team = Capstone_Team(course_section=section, project_no=1, capstone_team_id=1)
		new_cap_team.save()

def update_dept_head():
	file = os.path.join(settings.BASE_DIR, 'Professors.csv')
	with open(file) as f:
		lines = csv.DictReader(f)
		courses = []
		for row in lines:
			try:
				if row['Title'] == 'Head':
					dept = Department.objects.get(dept_id=row['Department'])
					dept.dept_head = row['Email']
					dept.save()
			except Exception as e:
				print(e)

def populate_professors():
	file = os.path.join(settings.BASE_DIR, 'Professors.csv')
	with open(file) as f:
		lines = csv.DictReader(f)
		courses = []
		for row in lines:
			try:
				first, last = row['Name'].split(" ", 1)
				new_user = User(first_name=first,
								last_name=last,
								username=row['Email'],
								password=make_password(row['Password']))
				new_user.save()

			except Exception as e:
				print(e)

			try:
				new_dept = Department(dept_id=row['Department'], 
										dept_name=row['Department Name'], 
										dept_head="")
				new_dept.save()	
			except Exception as e:
				new_dept = Department.objects.get(dept_id=row['Department'])
				print(e)

			team_id = int(float(row['Team ID']))

			try:
				new_prof = Professor(user=new_user, 
										email=row['Email'], 
										name=row['Name'], 
										age=row['Age'], 
										gender=row['Gender'],
										office_address=row['Office'],
										department=new_dept,
										title=row['Title'])
				new_prof.save()

				new_prof_teams = Prof_teams(teaching_team_id=team_id)
				new_prof_teams.save()
				
			except Exception as e:
				new_prof_teams = Prof_teams.objects.get(teaching_team_id=team_id)
				print(e)

			try:
				new_prof_teams_members = Prof_team_members(prof_email=row['Email'], teaching_team_id=new_prof_teams)
				new_prof_teams_members.save()
			except Exception as e:
				print(e)

			try:
				sections = Sections.objects.filter(course_id=row['Teaching'])	
				for section in sections:
					section.prof_team = Prof_teams.objects.get(teaching_team_id=team_id)
					section.save()

					if section.section_type == 'Cap':
						new_cap_section = Capstone_section(course_section=section, project_no=1, sponsor_id=row['Email'])
						new_cap_section.save()
			except Exception as e:
				print("error: ", e)

def populate_students():
	file = os.path.join(settings.BASE_DIR, 'Students.csv')
	with open(file) as f:
		lines = csv.DictReader(f)
		courses = dict()
		for row in lines:
			try:
				zip_code = Zipcode(zipcode=row['Zip'], 
									city=row['City'], 
									state=row['State'])
				zip_code.save()

				first, last = row['Full Name'].split(" ", 1)
				new_user = User(first_name=first,
								last_name=last,
								username=row['Email'],
								password=make_password(row['Password']))
				new_user.save()

				new_student = Student(user=new_user, 
										email=row['Email'], 
										name=row['Full Name'],
										age=row['Age'], 
										gender=row['Gender'], 
										major=row['Major'], 
										street=row['Street'], 
										zipcode=zip_code)
				new_student.save()
			except Exception as e:
				print('error with new student', e)

			all_courses_prefix = ['Course 1 ', 'Course 2 ', 'Course 3 ']
			for i in range(1,4):
				course_id = row['Courses ' + str(i)]
				course = 'Course ' + str(i)
				course_name = row[course + ' Name']
				course_description = row[course + ' Details']

				try:
					if course_id not in courses:
						new_course = Course(course_id=course_id, course_name=course_name, course_description=course_description)
						courses[course_id] = new_course
						new_course.save()
					else:
						new_course = courses[course_id]
				except Exception as e:
					print('new course:', e)

				section_type = row[course + ' Type']
				course_sec = int(float(row[course + ' Section']))
				course_sec_limit = int(float(row[course + ' Section Limit'])) 

				try:
					new_section = Sections(course_id=new_course, sec_no=course_sec, section_type=section_type, limit=course_sec_limit, prof_team=None)
					new_section.save()
				except Exception as e:
					new_section = Sections.objects.get(course_id=course_id, sec_no=course_sec)
					print('new section: ', e)

				if section_type == 'Cap':
					try:
						new_cap_section = Capstone_section(course_section=new_section, project_no=1, sponsor_id=None)
						new_cap_section.save()

						new_cap_team = Capstone_Team(course_section=new_section, project_no=1, capstone_team_id=1)
						new_cap_team.save()

						#new_cap_member = Capstone_Team_Members(student_email=row['Email'], capstone_team_id=1, course_section=new_section)
						#new_cap_member.save()
					except Exception as e:
						print(e)
				
				try:
					new_enrolls = Enrolls(student_email=row['Email'], course_section=new_section)
					new_enrolls.save()
				except Exception as e:
					print('new enroll: ', e)

				hw_no = row[course + ' HW_No']
				if hw_no:
					hw_details = row[course + ' HW_Details']
					hw_grade = float(row[course + ' HW_Grade'])
					hw_no = int(float(hw_no))

					try:
						new_hw = Homework(course_section=new_section, hw_no=hw_no, hw_details=hw_details)
						new_hw.save()

						new_hw_grade = Homework_grades(student_email=row['Email'], course_section=new_section, hw_no=new_hw, hw_grade=hw_grade)
						new_hw_grade.save()
					except Exception as e:
						print('new hw: ', e)

				exam_no = row[course + ' EXAM_No']
				if exam_no:
					exam_details = row[course + ' Exam_Details']
					exam_grade = float(row[course + ' EXAM_Grade'])
					exam_no = int(float(exam_no))

					try:
						new_exam = Exams(course_section=new_section, exam_no=exam_no, exam_details=exam_details)
						new_exam.save()

						new_exam_grade = Exam_grades(student_email=row['Email'], course_section=new_section, exam_no=new_exam, exam_grade=exam_grade)
						new_exam_grade.save()
					except Exception as e:
						print('new exam: ', e)

