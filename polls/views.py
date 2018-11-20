from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def index(request):
    return HttpResponse("hello, now you are in django web htmls successfully")


def detail(request, question_id):
    response = " you are looking at detail of %s."
    return HttpResponse(response % question_id)


def results(request, question_id):
    response = " you are looking at result of %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    response = " you are voting on %s."
    return HttpResponse(response % question_id)
