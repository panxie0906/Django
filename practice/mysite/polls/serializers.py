from django.form import widgets
from rest_framework import serializers
from polls.models import Snippet,LANGUAGE_CHOICE,STYLE_CHOICE

class SnippetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Snippet
		fields = ('id','title','code','lineos','language','style',)