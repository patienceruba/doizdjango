from django.shortcuts import render

# Create your views here.
def chatapp(request):
	return render(request, "chat/chat.html")