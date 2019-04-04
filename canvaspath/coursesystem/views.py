from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render

def home(request):
	return render(request,'coursesystem/home.html')

def signup(request):
	form = UserCreationForm
	successurl = reverse_lazy('login')
	return render(request, 'coursesystem/signup.html', {'form': form})