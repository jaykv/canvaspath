from django.contrib.auth.models import User
from django.conf import settings
from coursesystem.models import * 
from django.contrib.auth.hashers import make_password
import os, csv

def populate_professors():

def populate_students():
	file = os.path.join(settings.BASE_DIR, 'Students.csv')
	with open(file) as f:
		lines = csv.DictReader(f)
		courses = []
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

				all_courses_prefix = ['Course 1 ', 'Course 2 ', 'Course 3 ']
				for i in range(1,4):
					course_id = row['Courses ' + str(i)]
					course = 'Course ' + str(i)
					course_name = row[course + ' Name']
					course_description = row[course + ' Details']
					if course_id not in courses:
						new_course = Course(course_id=course_id, course_name=course_name, course_description=course_description)
						courses.append(course_id)

					section_type = row[course + ' Type']
					course_sec = row[course + ' Section']
					course_sec_limit = row[course + ' Section Limit'] 
					new_section = Sections(course_id=course_id, sec_no=course_sec, section_type=section_type, limit=course_sec_limit, prof_team=None)

					if course_type == 'Cap':
						new_cap_section = Capstone_section(course_id=course_id, sec_no=course_sec, project_no=1, sponsor_id=None)
						new_cap_team = Capstone_Team(course_id=course_id, sec_no=course_sec, project_no=1, capstone_team_id=1)
						new_cap_member = Capstone_Team_Members(student_email=row['Email'], capstone_team_id=1, course_id=course_id, sec_no=course_sec)
					
					new_enrolls = Enrolls(student_email=row['Email'], course_id=course_id, sec_no=course_sec)
					
					hw_no = row[course + ' HW_No']
					if hw_no != '':
						hw_details = row[course + ' HW_Details']
						hw_grade = row[course + ' HW_Grade']
						new_hw = Homework(course_id=course_id, sec_no=course_sec, hw_no=hw_no, hw_details=hw_details)
						new_hw_grade = Homework_grades(student_email=row['Email'], course_id=course_id, sec_no=course_sec, hw_no=hw_no, hw_grade=hw_grade)

					exam_no = row[course + ' EXAM_No']
					if exam_no != '':
						exam_details = row[course + ' Exam_details']
						exam_grade = row[course + ' EXAM_Grade']
						new_exam = Exams(course_id=course_id, sec_no=course_sec, exam_no=exam_no, exam_details=exam_details)
						new_exam_grade = Exam_grades(student_email=row['Email'], course_id=course_id, sec_no=course_sec, exam_no=exam_no, exam_grade=exam_grade)
			except:
		 		print("there was a problem with row", row)


