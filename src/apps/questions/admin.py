from django.contrib import admin
from .models import Difficulty, Question, TestCase, QuestionExample

admin.site.register(Difficulty)
admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(QuestionExample)
