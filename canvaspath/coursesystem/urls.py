from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
	path('',views.home,name='home'),
	path('student/',views.student_home,name='student_home'),
	path('faculty/',views.faculty_home,name='faculty_home'),
	path('admin/',views.admin_home,name='admin_home'),
	path('populate/',views.populate_data,name='populate_data'),
	# path('signup/',views.signup,name='signup'),
	url(r'^ajax/delete-hw/$', views.delete_hw, name='delete_hw'),
	url(r'^ajax/delete-exam/$', views.delete_exam, name='delete_exam'),
	url(r'^ajax/add-assignment/$', views.add_assignment, name='add_assignment'),
	url(r'^ajax/update-grades/$', views.update_grades, name='update_grades'),
]
