from django.shortcuts import render

# Create your views here.

def getform(request):
    return render(request, 'userform.html')