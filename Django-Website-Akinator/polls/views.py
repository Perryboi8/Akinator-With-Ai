from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .gpt4_chara import Genre, get_initial_question, get_next_question
import logging
from .llama_service import generate_next_question, make_guess, evaluate_confidence

logger = logging.getLogger(__name__)

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
    #redirects you to the 'next' page and to home page if next isnt there allows the url to be consistent across both
    next_page = request.GET.get('next', reverse('polls:home_page'))
    return redirect(next_page)


def guess_page(request):
   #place holder for the guess page to show it, You can add code here
   return render(request, 'guess.html')

def question_view_llama(request):
    if request.method == 'POST':
        # Retrieve or initialize session variables
        context = request.session.get('context', [])
        confidence = request.session.get('confidence', "0")
        iteration = request.session.get('iteration', 1)

        # User's response

        textbox_answer = request.POST.get('textbox-answer').strip()
        if textbox_answer:
          user_answer = request.POST.get('textbox-answer').strip()
        else:
          user_answer = request.POST.get('button-answer').strip()
        context.append(f"Answer {iteration + 1}: {user_answer}")

        # Generate the next question
        if not context:
           question = "Is your character real?"
           context.append(f"Question 1: : {question}")
        question = generate_next_question(context)
        context.append(f"Question {iteration + 1}: {question}")

        # Evaluate confidence
        confidence = evaluate_confidence(context)
        request.session['context'] = context
        request.session['confidence'] = confidence
        request.session['iteration'] = iteration + 1
        print(context)

        # Check if confidence is sufficient for a guess
        if confidence == "10" or iteration >= 10:
            guess = make_guess(context)
            return render(request, 'guess.html', {'guess': guess, 'confidence': confidence})

        # Continue with the next question
        return render(request, 'index2.html', {'ai_response': question, 'context': context, 'confidence': confidence})

    # Handle GET (start of the game)
    request.session['context'] = []
    request.session['confidence'] = "0"
    request.session['iteration'] = 0
    first_question = "Is your character real?"
    return render(request, 'index2.html', {'ai_response': first_question})


