from django.shortcuts import render

def fantasy(request):
    return render(request, 'base.html')

def draft(request):
    return render(request, 'draft.html')

def team(request):
    return render(request, 'team.html')

def standings(request):
    return render(request, 'standings.html')

def matchup(request):
    return render(request, 'matchup.html')


