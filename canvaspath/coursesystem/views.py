from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from . import populate

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


	return render(request,'coursesystem/home.html')

def signup(request):
	form = UserCreationForm
	successurl = reverse_lazy('login')
	return render(request, 'coursesystem/signup.html', {'form': form})