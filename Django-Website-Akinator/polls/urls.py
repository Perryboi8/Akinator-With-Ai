from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = "polls"
urlpatterns = [
    path("home", views.home_page),
    path("question", views.question_page, name = 'question_page')

]
