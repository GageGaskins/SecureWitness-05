from django.shortcuts import render
from django.http import HttpResponse

from django.template import RequestContext, loader

# Create your views here.


def index(request):
    return render(request, 'SecureWitness/index.html', {})


def user(request):
    return render(request, 'SecureWitness/user.html', {})