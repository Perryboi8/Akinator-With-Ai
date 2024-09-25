from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = "polls"

#Notice we pass the functions from views as reference
#This is a continuation of the home page so it would be like url.home/___
urlpatterns = [
    path("home", views.home_page),
    path("question", views.question_page),
]
