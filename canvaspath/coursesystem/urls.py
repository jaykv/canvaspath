from django.urls import include, path
from . import views

urlpatterns = [
	path('',views.home,name='home'),
	path('student/',views.student_home,name='student_home'),
	path('faculty/',views.faculty_home,name='faculty_home'),
	path('admin/',views.admin_home,name='admin_home'),
	path('populate/',views.populate_data,name='populate_data'),
	path('signup/',views.signup,name='signup'),
]
