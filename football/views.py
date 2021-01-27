from django.shortcuts import render
from .models import Players

def fantasy(request):
    return render(request, 'base.html')

def draft(request):
    players = Players.objects.all()
    context = {
        'players': players
    }
    return render(request, 'draft.html', context)

def team(request):
    return render(request, 'team.html')

def standings(request):
    return render(request, 'standings.html')

def matchup(request):
    return render(request, 'matchup.html')


