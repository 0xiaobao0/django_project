# coding=utf-8
from django.shortcuts import render
from .models import UserMessage


# Create your views here.

def getform(request):
    # all_messages = UserMessage.objects.filter(name = 'mrliu')
    # for message in all_messages:
    #     print message.email
    if request.method == 'POST':
        usermessage = UserMessage()
        usermessage.name = request.POST.get('name', '')
        usermessage.email = request.POST.get('email', '')
        usermessage.address = request.POST.get('address', '')
        usermessage.message = request.POST.get('message', '')
        if(usermessage.name and usermessage.email and usermessage.address and usermessage.message):
            usermessage.save()
        else:
            return render(request, 'userform.html')

    return render(request, 'userform.html')