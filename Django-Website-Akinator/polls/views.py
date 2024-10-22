from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

#Where we create functions to show which template to show based on the http request
def home_page(request):
  return render(request, 'home.html')

def question_view(request):
  if request.method == 'POST':

    button_answer = request.POST.get('button-answer') #Grabs the button answer from index.html
    textbox_answer = request.POST.get('textbox-answer') #Grabs Textbox answer from html

    answers = request.session.get('answers', [])

    if textbox_answer and textbox_answer.strip():
       answers.append(textbox_answer.strip())
    elif button_answer:
       answers.append(button_answer)

    print(answers)
    request.session['answers'] = answers

    return render(request, 'index.html')


  return render(request, 'index.html')


def get_answers(request):
    answers = request.session.get('answers', [])
    return HttpResponse(f'Answers that are being stored: {answers}')

def clear_answers(request):
   request.session.clear()
   return HttpResponse(f'Answers Are Now Cleared')
