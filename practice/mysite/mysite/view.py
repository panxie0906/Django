import datetime
from django.http import HttpResponse

def hello(request):
	return HttpResponse("Hello world!")
	
def showTime(request):
	now = datetime.datetime.now()
	html = "<html><body>The time now is %s</body></html>" %now
	return HttpResponse(html)