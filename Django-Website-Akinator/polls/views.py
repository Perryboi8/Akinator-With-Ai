from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

#Where we create functions to show which template to show based on the http request
def home_page(request):

  return render(request, 'home.html')

def question_page(request):
  if request.method == 'POST':
    answer = request.POST.get('answer')

    answers = request.session.get('answers', [])

    answers.append(answer)
    print(len(answers))
    request.session['answers'] = answers

    return render(request, 'index.html')
  return render(request, 'index.html')


def get_answers(request):
    answers = request.session.get('answers', [])
    return HttpResponse(f'Answers that are being stored: {answers}')
