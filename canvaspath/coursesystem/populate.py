from django.contrib.auth.models import User
from django.conf import settings
from coursesystem.models import * 
from django.contrib.auth.hashers import make_password
import os, csv

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

				# all_courses_prefix = ['Course 1 ', 'Course 2 ', 'Course 3 ']
				# all_courses_key  = ['Courses 1', 'Courses 2', 'Courses 3']
				# for i in range(1,4):
				# 	course_id = row['Courses ' + str(i)]
				# 	course = 'Course ' + str(i)
				# 	course_name = row[course + ' Name']
				# 	course_description = row[course + ' Details']
				# 	if course_id not in courses:
				# 		new_course = Course(course_id=course_id, course_name=course_name, course_description=course_description)
				# 		courses.append(course_id)
					
			except:
				# if the're a problem anywhere, you wanna know about it
		 		print("there was a problem with row", row)  


