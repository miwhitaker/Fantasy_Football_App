from django.shortcuts import render
from .models import Players
from .forms import DraftForm
from .teams import team_names

def fantasy(request):
    return render(request, 'base.html')

def draft(request):
    players = Players.objects.all().order_by('points')
    context = {
        'players': players,
        'team': team_names
    }
    
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DraftForm(request.POST)
            if form.is_valid():
                drafted = Players.objects.get()
                drafted.rostered_by = request.user.username
                drafted.save()
    return render(request, 'draft.html', context)

def team(request):
    return render(request, 'team.html')

def standings(request):
    return render(request, 'standings.html')

def matchup(request):
    return render(request, 'matchup.html')


