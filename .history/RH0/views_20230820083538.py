from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('this home')

def about(request):
    return HttpResponse('this about')