from django.urls import include, path
from . import views

urlpatterns = [
	path('',views.home,name='home'),
	path('populate/',views.populate_data,name='populate_data'),
	path('signup/',views.signup,name='signup'),
]
