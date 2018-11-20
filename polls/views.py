from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def  index(request):
    return HttpResponse("hello, now you are in django web htmls successfully")
