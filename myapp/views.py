from django.shortcuts import render ,HttpResponse

# Create your views here.
def hellowworld(request):
    return HttpResponse ("hellow world")