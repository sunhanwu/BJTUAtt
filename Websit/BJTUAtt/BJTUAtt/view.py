#from django.http import HttpResponse
from django.shortcuts import render,render_to_response
 
def hello(request):
    context={}
    context['hello']='hello world'
    
    return render(request,'render.html',context)

def plot(request):
    return render_to_response(request,'render.html')
