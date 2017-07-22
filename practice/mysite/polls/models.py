from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICE = sorted([(item[1][0],item[0])for item in LEXERS])
STYLE_CHOICE = sorted((item,item)for item in get_all_styles())

class Question(models.Model):
	question_text = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('date published')
	def _str_(self):
		return self.question_text
	def was_published_recently(self):
		return self.pub_date >= timezone.now()-datetime.timedelta(days=1)
	
class Choice(models.Model):
	question = models.ForeignKey(Question,on_delete = models.CASCADE)
	choice_text = models.CharField(max_length = 200)
	votes = models.IntegerField(default = 0)
	def _str_(self):
		return self.choice_text
		
class Person(models.Model):
	name = models.CharField(max_length=30)
	age = models.IntegerField()
	
class Snippet(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=100,blank=True,default='')
	code = models.TextField()
	lineos = models.BooleanField(default=False)
	language = models.CharField(choices=LANGUAGE_CHOICE,default='python',max_length=100)
	style = models.CharField(choices=STYLE_CHOICE,default='friendly',max_length=100)
	
	class Meta:
		ordering=('created',)