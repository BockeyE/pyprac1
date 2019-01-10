from django.contrib import admin

# Register your models here.
from polls.models import Question



class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']



# register for model
admin.site.register(Question, QuestionAdmin)
