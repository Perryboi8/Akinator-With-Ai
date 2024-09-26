from django.shortcuts import render, redirect
from django.http import HttpResponse

def home_page(request):

  return render(request, 'home.html')

def question_page(request):
  if (request.method =="POST"):
    user_response = request.POST.get('response')

    if user_response =='yes':
      print("The user selected Yes")
    elif user_response == 'no':
      print("The user selected No")
    elif user_response == 'idk':
      print("the user selected idk")

    return redirect('question_page')

  return render(request, 'index.html')
