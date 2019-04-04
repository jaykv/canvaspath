from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from . import populate

def home(request):
	if request.GET.get('populate') == 'yes':
		populate.populate_students()
	return render(request,'coursesystem/home.html')

def signup(request):
	form = UserCreationForm
	successurl = reverse_lazy('login')
	return render(request, 'coursesystem/signup.html', {'form': form})