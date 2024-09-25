from django.shortcuts import render
from django.http import HttpResponse

#Where we create functions to show which template to show based on the http request
def home_page(request):
  return render(request, 'home.html')

def question_page(request):
  return render(request, 'index.html')
