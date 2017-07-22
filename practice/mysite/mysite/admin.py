from django.contrib import admin
from .models import Question,Choice,Person

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3
	
class PersonInline(admin.TabularInline):
	model = Person
	extra = 3
	
class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
	(None,{'fields':['question_text']}),
	('Data information',{'fields':['pub_date'],'classes':['collapse']}),
	]
	inlines = [ChoiceInline,PersonInline]
	list_display =('question_text','pub_date')
	
	
admin.site.register(Choice,Person)
admin.site.register(Question,QuestionAdmin)