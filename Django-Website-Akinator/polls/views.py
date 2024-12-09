from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .gpt4_chara import get_next_question, make_final_guess, evaluate_genre_confidence, identify_genre
import logging
from .llama_service import generate_next_question, make_guess, evaluate_confidence, generate_image

logger = logging.getLogger(__name__)

#Where we create functions to show which template to show based on the http request
def home_page(request):
  return render(request, 'home.html')

def question_view_gpt(request):
    if request.method == 'POST':
        button_answer = request.POST.get('button-answer')
        textbox_answer = request.POST.get('textbox-answer')
        answers = request.session.get('answers', [])
        previous_questions = request.session.get('previous_questions', [])
        iteration = request.session.get('iteration', 0)
        genre_confidence = request.session.get('genre_confidence', 0)
        genre_identified = request.session.get('genre_identified', False)
        log = request.session.get('log', "")

        if textbox_answer and textbox_answer.strip():
            answers.append(textbox_answer.strip())
        elif button_answer:
            answers.append(button_answer)

        iteration += 1
        log += f"Question {iteration}: {previous_questions[-1] if previous_questions else 'N/A'}, Answer: {answers[-1]}\n"
        request.session['iteration'] = iteration
        request.session['log'] = log
        request.session['answers'] = answers

        if not genre_identified and iteration >= 4:
            genre_confidence = evaluate_genre_confidence(log)
            if genre_confidence >= 85 or iteration >= 10:
                genre_description = identify_genre(log)
                log += f"\nGenre Identified: {genre_description}\n"
                request.session['log'] = log
                request.session['genre_identified'] = True
                request.session['iteration'] = 0
                answers = []
                previous_questions = []

        if genre_identified and iteration >= 4:
            final_guess = make_final_guess(log)
            return render(request, 'guess.html', {
                'final_guess': final_guess,
                'answers': answers,
                'iteration': iteration,
            })

        log = "\n".join(answers)
        question = None
        retry_limit = 10
        for _ in range(retry_limit):
            question = get_next_question(log, previous_questions)
            if question:
                previous_questions.append(question)
                break

        if not question:
            question = "I couldn't generate a new question. Try again later."

        request.session['previous_questions'] = previous_questions

        return render(request, 'index.html', {
            'ai_response': question,
            'answers': answers,
            'iteration': iteration,
        })

    # initializing
    request.session['iteration'] = 0
    request.session['answers'] = []
    request.session['previous_questions'] = []
    request.session['genre_confidence'] = 0
    request.session['genre_identified'] = False
    request.session['log'] = ""
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
   context = request.session.get('context', [])

   guess = make_guess(context)

   prompt = f"A image of the character {guess}, digital art"
   image_url = generate_image(prompt)
   
   print("Image URL:", image_url)

   return render(request, 'guess.html', {'final_guess': guess, 'image_url': image_url})

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
        if confidence == "10" or iteration >= 15:
            return redirect('polls:guessPage')

        # Continue with the next question
        return render(request, 'index2.html', {'ai_response': question, 'context': context, 'confidence': confidence})

    # Handle GET (start of the game)
    request.session['context'] = []
    request.session['confidence'] = "0"
    request.session['iteration'] = 0
    first_question = "Is your character real?"
    return render(request, 'index2.html', {'ai_response': first_question})
