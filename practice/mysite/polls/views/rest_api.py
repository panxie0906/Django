from rest_framework import viewsets,serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Mate:
		model = User
		fields = ('url','username','email','is_staff')

class TaskInstanceViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	pass