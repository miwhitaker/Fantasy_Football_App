from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Players, Week, Record
from .forms import DraftForm
from .teams import team_names
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.views import auth_login

ONLINE_THRESHOLD = getattr(settings, 'ONLINE_THRESHOLD', 60 * 90)

def fantasy(request):
    return render(request, 'base.html')

def lobby(request):
    if not request.user.is_authenticated:
        return (redirect('django.contrib.auth.views.login'))
    draft_list = [request.user.username, 'Emerald', 'LinearJS', 'JavasCrypt', 'Anaconda', 'HTMLdude']
    context = {
        'draft_list': draft_list,
    }

    return render(request, 'lobby.html')

### This is the homepage for a new fantasy football draft. Users have to be logged in for the app to work,
### so I have a redirect if they are not logged in. The draft list is managed by get_draft_list

def draft(request):
    if not request.user.is_authenticated:
        return (redirect('auth_login'))
    players = Players.objects.all().order_by('-points')
    draft_list = get_draft_list(request.user.username)
    if request.method == "POST" and 'reset' in request.POST:
        all_players = Players.objects.all()
        
        for player in all_players:
            player.rostered_by = '0'
            player.save()

        Record.objects.all().delete()
    
### This is what happens when user drafts a player - we make sure it is their turn on line 40 and that you have
### space on your roster for the player on line 42. Then this is saved and the draft list is updated in the function
### get_draft_list. After a user picks a player, their name is removed from the draft list (from top of list)
    if request.method == "POST" and 'draft' in request.POST:
        form = DraftForm(request.POST)
        if form.is_valid():
            if not draft_list:
                messages.add_message(request, messages.ERROR, f"The draft is complete")
            elif draft_list[0] == request.user.username: 
                drafted = Players.objects.get(pk = form.cleaned_data['player_id'])
                if check_player_list(drafted, request.user.username):
                    drafted.rostered_by = request.user.username
                    drafted.save()
                    draft_list = get_draft_list(request.user.username, True)
                    messages.add_message(request, messages.SUCCESS, f"{request.user.username} has drafted {drafted.name}")
                    draft_list = cpu_draft(request, draft_list)
                else:
                    messages.add_message(request, messages.ERROR, f"You already have a {drafted.position}")
            else:
                messages.add_message(request, messages.ERROR, f"It is not your turn to draft.") 

### The function: get_my_players retrieves the user's players from the database
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
    if not request.user.is_authenticated:
        return (redirect('auth_login'))
    week = get_week()
    user_list = [
                request.user.username,
                'Emerald',
                'LinearJS',
                'JavasCrypt',
                'Anaconda',
                'HTMLdude'
                ]

    all_matchups = get_all_matchups(user_list)
    all_matchups_dict = {
        't1': all_matchups['wk' + str(week)][0],
        't2': all_matchups['wk' + str(week)][1],
        't3': all_matchups['wk' + str(week)][2],
        't4': all_matchups['wk' + str(week)][3],
        't5': all_matchups['wk' + str(week)][4],
        't6': all_matchups['wk' + str(week)][5],
    }

    ### This calls the function get_team_stats, which returns statistics for a given player and week number
    stats = []
    for team in all_matchups['wk' + str(week)]:
        team_stats = get_team_stats(team, week)
        stats.append(team_stats)
    
    all_stats = {
        't1': stats[0],
        't2': stats[1],
        't3': stats[2],
        't4': stats[3],
        't5': stats[4],
        't6': stats[5],
    }

    total_pts = []
    for team in stats:
        team_total = team['qb'].points + team['rb'].points + team['wr'].points
        total_pts.append(team_total)
    
    total = {
        't1': total_pts[0],
        't2': total_pts[1],
        't3': total_pts[2],
        't4': total_pts[3],
        't5': total_pts[4],
        't6': total_pts[5],
    }

### This controls the win/loss records for all users. This is posted to the Record database. It also moves forward to
### the next week when the "advance" button is clicked. The first time through, it creates a DB record for each user.
    if request.method == "POST":
        week = get_week()
        if week < 5:
            increment_week = True
            for user in all_matchups['wk' + str(week)]:
                try:
                    user_record = Record.objects.get(username = user)
                    if increment_week:
                        week = get_week(True)
                        increment_week = False
                    user_record.week = week
                    user_record.save()
                except Record.DoesNotExist:
                    records = Record.objects.create(
                                   week = week,
                                   username = user,
                                   win = 0,
                                   loss = 0,
                                   tie = 0,
                                   points = 0,
                                   )
                    records.save()
            check_winner(total['t1'], total['t2'], all_matchups_dict['t1'], all_matchups_dict['t2'])
            check_winner(total['t3'], total['t4'], all_matchups_dict['t3'], all_matchups_dict['t4'])
            check_winner(total['t5'], total['t6'], all_matchups_dict['t5'], all_matchups_dict['t6'])
        else:
            pass

    all_records = Record.objects.filter(week = week).order_by('-win')

    context = {
        'user_list': user_list,
        'total': total,
        'all_matchups': all_matchups_dict,
        'all_stats': all_stats,
        'all_records': all_records,
        'week': week
    }
    return render(request, 'standings.html', context)

def matchup(request):
    if not request.user.is_authenticated:
        return (redirect('auth_login'))
    week = get_week()
    user_list = [
                request.user.username,
                'Emerald',
                'LinearJS',
                'JavasCrypt',
                'Anaconda',
                'HTMLdude'
                ]

    all_matchups = get_all_matchups(user_list)
    all_matchups_dict = {
        't1': all_matchups['wk' + str(week)][0],
        't2': all_matchups['wk' + str(week)][1],
        't3': all_matchups['wk' + str(week)][2],
        't4': all_matchups['wk' + str(week)][3],
        't5': all_matchups['wk' + str(week)][4],
        't6': all_matchups['wk' + str(week)][5],
    }
    
### This calls the function get_team_stats, which returns statistics for a given player and week number. From there we
### figure out how many points every fantasy team scored in a week
    stats = []
    for team in all_matchups['wk' + str(week)]:
        team_stats = get_team_stats(team, week)
        stats.append(team_stats)
    
    all_stats = {
        't1': stats[0],
        't2': stats[1],
        't3': stats[2],
        't4': stats[3],
        't5': stats[4],
        't6': stats[5],
    }

    total_pts = []
    for team in stats:
        team_total = team['qb'].points + team['rb'].points + team['wr'].points
        total_pts.append(team_total)
    
    total = {
        't1': total_pts[0],
        't2': total_pts[1],
        't3': total_pts[2],
        't4': total_pts[3],
        't5': total_pts[4],
        't6': total_pts[5],
    }

    context = {
        'user_list': user_list,
        'total': total,
        'all_matchups': all_matchups_dict,
        'all_stats': all_stats,
        'week': week
    }

    return render(request, 'matchup.html', context)

### This populates a list of all NFL players the user has drafted up to this point -- it calls the Players database
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
### The CPU checks each position to see if it has a player - if not, pick one at that position from the top of the list
def cpu_draft(request, draft_list):
    for user in draft_list:
        if user == request.user.username:
            return draft_list
        cpu_players = get_my_players(user)

        if cpu_players['qb'] == '0':
            player = Players.objects.filter(rostered_by = '0', position = 'QB').order_by('-points').first()
            player.rostered_by = user
            player.save()
            messages.add_message(request, messages.SUCCESS, f"{user} has drafted {player.name}")
            draft_list = get_draft_list(user, True)
        
        elif cpu_players['rb'] == '0':
            player = Players.objects.filter(rostered_by = '0', position = 'RB').order_by('-points').first() 
            player.rostered_by = user
            player.save()
            messages.add_message(request, messages.SUCCESS, f"{user} has drafted {player.name}")
            draft_list = get_draft_list(user, True)

        elif cpu_players['wr'] == '0':
            player = Players.objects.filter(rostered_by = '0', position = 'WR').order_by('-points').first()
            player.rostered_by = user
            player.save()
            messages.add_message(request, messages.SUCCESS, f"{user} has drafted {player.name}")
            draft_list = get_draft_list(user, True)

    return draft_list

### This function collects stats for an individual user for a specific week. It calls the get_my_players function 
### to get list of user's player names and position, then matches those up with the stats stored in the 'Week' DB
def get_team_stats(user, week):
    user_players = get_my_players(user)
    user_stats_qb = Week.objects.filter(
                                        week = week, 
                                        name = user_players['qb'].name,
                                        position = 'QB')
    
    user_stats_rb = Week.objects.filter(
                                        week = week, 
                                        name = user_players['rb'].name,
                                        position = 'RB')

    user_stats_wr = Week.objects.filter(
                                        week = week, 
                                        name = user_players['wr'].name,
                                        position = 'WR')

    user_stats = {
                'qb': user_stats_qb[0],
                'rb': user_stats_rb[0],
                'wr': user_stats_wr[0]
                }

    return user_stats

### This is just the dictionary for which teams are playing against each other each week
def get_all_matchups(user_list):
    all_matchups = {'wk1': [user_list[0],
                            user_list[1],
                            user_list[2],
                            user_list[3],
                            user_list[4],
                            user_list[5]],
                    'wk2': [user_list[0],
                            user_list[2],
                            user_list[1],
                            user_list[5],
                            user_list[3],
                            user_list[4]],
                    'wk3': [user_list[0],
                            user_list[3],
                            user_list[1],
                            user_list[4],
                            user_list[2],
                            user_list[5]],
                    'wk4': [user_list[0],
                            user_list[4],
                            user_list[1],
                            user_list[2],
                            user_list[3],
                            user_list[5]],
                    'wk5': [user_list[0],
                            user_list[5],
                            user_list[1],
                            user_list[3],
                            user_list[2],
                            user_list[4]],
                    }
    return all_matchups

### This controls the current week. It defaults to week one until user advances to the next week
def get_week(next_week = False):
    curr_week = cache.get('current_week', 1)
    if next_week and curr_week < 5:
        curr_week += 1
    cache.set('current_week', curr_week, ONLINE_THRESHOLD)
    return curr_week

### This checks the numbers that are sent in for two teams (total1 and total2) to see who wins (u1 or u2). This needs to 
### be called 3 times per week as there are 3 matchups per week. Results saved in Record DB
def check_winner(total1, total2, u1, u2):
    week = get_week()
    records_u1 = Record.objects.get(week = week, username = u1)
    records_u2 = Record.objects.get(week = week, username = u2)

    if total1 > total2:
        records_u1.win += 1
        records_u2.loss += 1
    elif total2 > total1:
        records_u1.loss += 1
        records_u2.win += 1
    elif total1 == total2:
        records_u1.tie += 1
        records_u2.tie += 1

    records_u1.points = records_u1.points + total1
    records_u2.points = records_u2.points + total2
    records_u1.save()
    records_u2.save()
