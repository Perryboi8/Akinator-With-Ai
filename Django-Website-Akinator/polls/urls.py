from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = "polls"

#Notice we pass the functions from views as reference
#This is a continuation of the home page so it would be like url.home/___
urlpatterns = [
    path('', views.home_page, name= 'home_page'),
    path('question-gpt', views.question_view_gpt, name='question_page_gpt'),
    path('get-answers', views.get_answers, name='get_page'),
    path('clear-answers', views.clear_answers, name='clear_page'),
    path('guess', views.guess_page, name='guessPage'),
    path('question-llama', views.question_view_llama, name = 'question_page_llama')
]
