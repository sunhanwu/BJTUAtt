from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'AttSystem/index.html', {'hello': 'BJTUAtt'})

def test2(request):
    return render(request,'AttSystem/test2.html')



# Create your views here.
