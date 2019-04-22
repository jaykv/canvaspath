from django.contrib.auth.models import User
from django.conf import settings
from coursesystem.models import * 
from django.contrib.auth.hashers import make_password
import os, csv

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

				new_prof = Professor(user=new_user, 
										email=row['Email'], 
										name=row['Name'], 
										age=row['Age'], 
										gender=row['Gender'],
										office_address=row['Office'],
										department=row['Department'],
										title=row['Title'])

				new_prof.save()

				if row['Title'] == 'Head':
					new_dept = Department(dept_id=row['Department'], dept_name=row['Department Name'], dept_head=new_prof)
					new_dept.save()

			except:
				print("there was a problem with row", row)

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
			except:
				print('error with new student\n')

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
				course_sec_id = course_id + '-' + str(course_sec)
				courses_sec_dict = dict()
				try:
					if course_sec_id not in courses_sec_dict:
						new_section = Sections(course_id=new_course, sec_no=course_sec, section_type=section_type, limit=course_sec_limit, prof_team=None)
						new_section.save()

						courses_sec_dict[course_sec_id] = new_section
					else:
						new_section = courses_sec_dict[course_sec_id]

				except Exception as e:
					print('new section: ', e)

				if section_type == 'Cap':
					try:
						new_cap_section = Capstone_section(course_id=new_course, sec_no=new_section, project_no=1, sponsor_id=None)
						new_cap_team = Capstone_Team(course_id=new_course, sec_no=new_section, project_no=1, capstone_team_id=1)
						#new_cap_member = Capstone_Team_Members(student_email=row['Email'], capstone_team_id=1, course_id=new_course, sec_no=new_section)
						
						new_cap_section.save()
						new_cap_team.save()
						#new_cap_member.save()
					except Exception as e:
						print(e)
				
				try:
					new_enrolls = Enrolls(student_email=row['Email'], course_id=new_course, sec_no=new_section)
					new_enrolls.save()
				except Exception as e:
					print('new enroll: ', e)

				hw_no = row[course + ' HW_No']
				if hw_no != '':
					hw_details = row[course + ' HW_Details']
					hw_grade = row[course + ' HW_Grade']
					
					try:
						new_hw = Homework(course_id=new_course, sec_no=new_section, hw_no=hw_no, hw_details=hw_details)
						new_hw_grade = Homework_grades(student_email=row['Email'], course_id=new_course, sec_no=new_section, hw_no=new_hw, hw_grade=hw_grade)

						new_hw.save()
						new_hw_grade.save()
					except Exception as e:
						print('new hw: ', e)

				exam_no = row[course + ' EXAM_No']
				if exam_no != '':
					exam_details = row[course + ' Exam_Details']
					exam_grade = row[course + ' EXAM_Grade']
					
					try:
						new_exam = Exams(course_id=new_course, sec_no=new_section, exam_no=exam_no, exam_details=exam_details)
						new_exam_grade = Exam_grades(student_email=row['Email'], course_id=new_course, sec_no=new_section, exam_no=new_exam, exam_grade=exam_grade)
						
						new_exam.save()
						new_exam_grade.save()
					except Exception as e:
						print('new exam: ', e)

