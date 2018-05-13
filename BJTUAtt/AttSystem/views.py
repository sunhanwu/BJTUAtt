from django.shortcuts import render
from django.http import HttpResponse
from . import models


def index(request):
    return render(request, 'AttSystem/index.html', {'hello': 'BJTUAtt'})

def test2(request):
    return render(request,'AttSystem/test2.html')

def show(request):
    pass



# Create your views here.
