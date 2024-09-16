from django.contrib import admin

# Register your models here.

from .models import Question #sends the model to be editable on the admin interface
admin.site.register(Question)
