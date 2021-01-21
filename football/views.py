from django.shortcuts import render


def index(request):
    return render(request, 'fantasy.html')

def base(request):
    return render(request, 'base.html')

def fantasy(request):
    return render(request, 'fantasy.html')

