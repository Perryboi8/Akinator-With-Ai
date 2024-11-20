from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .gpt4_chara import Genre, get_initial_question, get_next_question

#Where we create functions to show which template to show based on the http request
def home_page(request):
  return render(request, 'home.html')

def question_view_gpt(request):
  if request.method == 'POST':

    button_answer = request.POST.get('button-answer') #Grabs the button answer from index.html
    textbox_answer = request.POST.get('textbox-answer') #Grabs Textbox answer from html

    answers = request.session.get('answers', [])
    previous_questions = request.session.get('previous_questions', [])


    if textbox_answer and textbox_answer.strip():
       answers.append(textbox_answer.strip())
    elif button_answer:
       answers.append(button_answer)

    print(answers)
    request.session['answers'] = answers

    log = "\n".join(answers)


    while True:
      question = get_next_question(log)

      if question not in previous_questions:
         previous_questions.append(question)
         break

    request.session['previous_questions'] = previous_questions

    return render(request, 'index.html', {'ai_response': question, 'answers': answers})


  return render(request, 'index.html')


def get_answers(request):
    answers = request.session.get('answers', [])
    return HttpResponse(f'Answers that are being stored: {answers}')

def clear_answers(request):
   request.session.clear()
   return HttpResponse(f'Answers Are Now Cleared')


def guess_page(request):
   #place holder for the guess page to show it, You can add code here




   return render(request, 'guess.html')

def question_view_llama(request):
  if request.method == 'POST':

    button_answer = request.POST.get('button-answer') #Grabs the button answer from index.html
    textbox_answer = request.POST.get('textbox-answer') #Grabs Textbox answer from html

    answers = request.session.get('answers', [])
    previous_questions = request.session.get('previous_questions', [])


    if textbox_answer and textbox_answer.strip():
       answers.append(textbox_answer.strip())
    elif button_answer:
       answers.append(button_answer)

    print(answers)
    request.session['answers'] = answers

    log = "\n".join(answers)


    while True:
      question = get_next_question(log)

      if question not in previous_questions:
         previous_questions.append(question)
         break

    request.session['previous_questions'] = previous_questions

    return render(request, 'index2.html', {'ai_response': question, 'answers': answers})


  return render(request, 'index2.html')
