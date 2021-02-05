from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Players, Week
from .forms import DraftForm
from .teams import team_names
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from django.conf import settings

ONLINE_THRESHOLD = getattr(settings, 'ONLINE_THRESHOLD', 60 * 90)

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

### This is the homepage for a new fantasy football draft. Users have to be logged in for the app to work,
### so I have a redirect if they are not logged in. The draft list is managed by function call lower on page

def draft(request):
    if not request.user.is_authenticated:
        return (redirect('django.contrib.auth.views.login'))
    players = Players.objects.all().order_by('-points')
    draft_list = get_draft_list(request.user.username)
    
### This is what happens when user drafts a player - we make sure it is their turn on line 40 and that you have
### space on your roster for the player on line 42. Then this is saved and the draft list is updated in the function
### get_draft_list. After a user picks a player, their name is removed from the draft list (from top of list)
    if request.method == "POST":
        form = DraftForm(request.POST)
        if form.is_valid():
            if draft_list[0] == request.user.username: 
                drafted = Players.objects.get(pk = form.cleaned_data['player_id'])
                if check_player_list(drafted, request.user.username):
                    drafted.rostered_by = request.user.username
                    drafted.save()
                    draft_list = get_draft_list(request.user.username, True)
                    messages.add_message(request, messages.SUCCESS, f"You just drafted {drafted.name}")
                    draft_list = cpu_draft(request, draft_list)
                else:
                    messages.add_message(request, messages.ERROR, f"You already have a {drafted.position}")
            else:
                messages.add_message(request, messages.ERROR, f"It is not your turn to draft. It is {draft_list[0]}'s turn") 

    my_players = get_my_players(request.user.username)
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
    
    return render(request, 'draft.html', context)


def standings(request):
    return render(request, 'standings.html')

def matchup(request):
    week = 1
    user_list = [
                request.user.username,
                'Emerald',
                'LinearJS',
                'JavasCrypt',
                'Anaconda',
                'HTMLdude'
                ]

    all_matchups = {'wk1': {'t1': user_list[0],
                                't2': user_list[1],
                                't3': user_list[2],
                                't4': user_list[3],
                                't5': user_list[4],
                                't6': user_list[5]},
                    'wk2': {'t1': user_list[0],
                                't2': user_list[2],
                                't3': user_list[1],
                                't4': user_list[5],
                                't5': user_list[3],
                                't6': user_list[4]},
                    'wk3': {'t1': user_list[0],
                                't2': user_list[3],
                                't3': user_list[1],
                                't4': user_list[4],
                                't5': user_list[2],
                                't6': user_list[5]},
                    'wk4': {'t1': user_list[0],
                                't2': user_list[4],
                                't3': user_list[1],
                                't4': user_list[2],
                                't5': user_list[3],
                                't6': user_list[5]},
                    'wk5': {'t1': user_list[0],
                                't2': user_list[5],
                                't3': user_list[1],
                                't4': user_list[3],
                                't5': user_list[2],
                                't6': user_list[4]},
                    }
    
### This calls the function get_team_stats, which returns statistics for a given player and week number
    user_stats = get_team_stats(all_matchups['wk1']['t1'], week)
    team2_stats = get_team_stats(all_matchups['wk1']['t2'], week)
    team3_stats = get_team_stats(all_matchups['wk1']['t3'], week)
    team4_stats = get_team_stats(all_matchups['wk1']['t4'], week)
    team5_stats = get_team_stats(all_matchups['wk1']['t5'], week)
    team6_stats = get_team_stats(all_matchups['wk1']['t6'], week)
    
    context = {
        'user_list': user_list,
        'user_stats': user_stats,
        'team2_stats': team2_stats,
        'team3_stats': team3_stats,
        'team4_stats': team4_stats,
        'team5_stats': team5_stats,
        'team6_stats': team6_stats,
        'all_matchups': all_matchups['wk{week}'],
    }

    return render(request, 'matchup.html', context)

### This populates a list of all players the user has drafted up to this point -- it calls the Players database
def get_my_players(user):
    try: 
        my_qb = Players.objects.get(rostered_by = user, position = 'QB')
    except Players.DoesNotExist:
        my_qb = '0'
    try: 
        my_rb = Players.objects.get(rostered_by = user, position = 'RB')
    except Players.DoesNotExist:
        my_rb = '0'
    try: 
        my_wr = Players.objects.get(rostered_by = user, position = 'WR')
    except Players.DoesNotExist:
        my_wr = '0'
    my_players = {'qb': my_qb, 
                'rb': my_rb, 
                'wr': my_wr}
    return my_players

### This is a check to make sure you only have 1 player for each position - true means you can draft the player
def check_player_list(plyr, user):
    my_players = get_my_players(user)
    player_check = my_players[plyr.position.lower()]
    if player_check == '0':
        return True
    else:
        return False

### This manages the draft list, it removes the user who just chose a player and returns the remaining list. The first
### time through, it just returns the original list
def get_draft_list(user, next_user = False):
    draft_list = [user, 'Emerald', 'LinearJS', 'JavasCrypt', 'Anaconda', 'HTMLdude', 'HTMLdude', 'Anaconda', 'JavasCrypt', 'LinearJS', 'Emerald', user, user, 'Emerald', 'LinearJS', 'JavasCrypt', 'Anaconda', 'HTMLdude']
    draft_list = cache.get('draft_list', draft_list)
    if next_user:
        draft_list.pop(0)
    cache.set('draft_list', draft_list, ONLINE_THRESHOLD)
    return draft_list

### This handles the cpu draft selection. It tells them to choose the player at the top of the list for each position.
### The CPU checks each position to see if it has a player - if not pick one at that position from the top of the list
def cpu_draft(request, draft_list):
    for user in draft_list:
        if user == request.user.username:
            return draft_list
        cpu_players = get_my_players(user)

        if cpu_players['qb'] == '0':
            player = Players.objects.filter(rostered_by = '0', position = 'QB').order_by('-points').first()
            player.rostered_by = user
            player.save()
            draft_list = get_draft_list(user, True)
        
        elif cpu_players['rb'] == '0':
            player = Players.objects.filter(rostered_by = '0', position = 'RB').order_by('-points').first() 
            player.rostered_by = user
            player.save()
            draft_list = get_draft_list(user, True)

        elif cpu_players['wr'] == '0':
            player = Players.objects.filter(rostered_by = '0', position = 'WR').order_by('-points').first()
            player.rostered_by = user
            player.save()
            draft_list = get_draft_list(user, True)

    return draft_list

### This function collects stats for an individual user for a specific week. It calls the get_my_players function 
### to get list of user's player names and position, then matches those up with the stats stored in the 'Week' DB
def get_team_stats(user, week):
    user_players = get_my_players(user)
    try:
        user_stats_qb = Week.objects.filter(
                                        week = week, 
                                        name = user_players['qb'].name,
                                        position = 'QB')
    except Week.DoesNotExist:
        user_stats_qb = '0'
    
    try:
        user_stats_rb = Week.objects.filter(
                                        week = week, 
                                        name = user_players['rb'].name,
                                        position = 'RB')
    except Week.DoesNotExist:
        user_stats_rb = '0'

    try:
        user_stats_wr = Week.objects.filter(
                                        week = week, 
                                        name = user_players['wr'].name,
                                        position = 'WR')
    except Week.DoesNotExist:
        user_stats_rb = '0'

    user_stats = {
                'qb': user_stats_qb[0],
                'rb': user_stats_rb[0],
                'wr': user_stats_wr[0]
                }
    return user_stats

