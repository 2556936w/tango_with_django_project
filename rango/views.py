from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    message = "Rango says hey there partner!<br><a href='/rango/about/'>About</a>"
    return HttpResponse(message)

def about(request):
    message = "Rango says here is the about page.<br><a href='/rango/'>Index</a>"
    return HttpResponse(message)
