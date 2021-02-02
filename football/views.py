from django.shortcuts import render, redirect
from .models import Players
from .forms import DraftForm
from .teams import team_names
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache

def fantasy(request):
    return render(request, 'base.html')

def lobby(request):
    if not request.user.is_authenticated:
        return (redirect('django.contrib.auth.views.login'))
    draft_list = [request.user.username, 'FootballAce', 'BotArmy', 'JSguru', 'ThePythons', 'HTMLwhiz']

    context = {
        'draft_list': draft_list,
    }

    return render(request, 'lobby.html')


def draft(request):
    if not request.user.is_authenticated:
        return (redirect('django.contrib.auth.views.login'))
    players = Players.objects.all().order_by('-points')
    
    def get_my_players():
        try: 
            my_qb = Players.objects.get(rostered_by = request.user.username, position = 'QB')
        except Players.DoesNotExist:
            my_qb = '0'
        try: 
            my_rb = Players.objects.get(rostered_by = request.user.username, position = 'RB')
        except Players.DoesNotExist:
            my_rb = '0'
        try: 
            my_wr = Players.objects.get(rostered_by = request.user.username, position = 'WR')
        except Players.DoesNotExist:
            my_wr = '0'
        my_players = {'qb': my_qb, 
                    'rb': my_rb, 
                    'wr': my_wr}
        return my_players
    
    def check_player_list(plyr):
        my_players = get_my_players()
        player_check = my_players[plyr.position.lower()]
        if player_check == '0':
            return True
        else:
            return False
        
    draft_list = [request.user.username, 'FootballAce', 'BotArmy', 'JSguru', 'ThePythons', 'HTMLwhiz', 'HTMLwhiz', 'ThePythons', 'JSguru', 'BotArmy', 'FootballAce', request.user.username, request.user.username, 'FootballAce', 'BotArmy', 'JSguru', 'ThePythons', 'HTMLwhiz']

    my_players = get_my_players()
    my_qb = my_players['qb']
    my_rb = my_players['rb']
    my_wr = my_players['wr']

    context = {
        'players': players,
        'my_qb': my_qb,
        'my_rb': my_rb,
        'my_wr': my_wr,
        'form': DraftForm(),
        'draft_list': draft_list,
    }
    
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DraftForm(request.POST)
            if form.is_valid():
                if draft_list[0] == request.user.username:
                    drafted = Players.objects.get(pk = form.cleaned_data['player_id'])
                    if check_player_list(drafted):
                        drafted.rostered_by = request.user.username
                        drafted.save()
                        draft_list.pop(0)
                    else:
                        return("You already have a", drafted.position)
                else:
                    return ('It is not your turn to draft a player')

    return render(request, 'draft.html', context)

def team(request):
    return render(request, 'team.html')

def standings(request):
    return render(request, 'standings.html')

def matchup(request):
    return render(request, 'matchup.html')



