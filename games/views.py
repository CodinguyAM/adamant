from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from datetime import datetime as time
from .models import User, Game, Player
from .logic import *


import random

# Create your views here.

allowed = [
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    ' ',
    'BCDFGHKLMNPRSTVWZ',
    'AEIOU',
    'BCDFGJKLMNPRSTVXZ',
    ' ',
    '123456789AEIOU',
    '123456789BCDFGHJKLMNPQRSTVWXZ',
]

TLI = {
    'ADW': 'Adverdle',
}

def code(i, L):
    global allowed
    #
    random.seed(time.now().strftime('%z %f %S %m %H %d %M %Y') + str(i))
    #
    r = ''
    #
    for l in range(L):
        r += random.choice(allowed[l])
    #
    return r

def ndigint(i, L):
    random.seed(time.now().strftime('%z %f %S %m %H %d %M %Y') + str(i))
    r = 0
    for l in range(L):
        r *= 10
        r += int(random.random() * 10)
    return r

def warn(msg):
    with open('zwarnings.txt', 'a') as fhand:
        fhand.write(time.now().strftime('@%d-%m-%Y: %H:%M:%S.%f (%Z=%:z) - '))
        fhand.write(msg)
        fhand.write('\n')
        
def get_settings(request):
    # Get settings. I mean, it's in the name. Exactly which settings - the names are again self-explanatory.
    user = User.objects.filter(username=request.GET['u']).first()

    if (not user) or (user != request.user):
        warn(f"Attempt to access settings of {user} by {request.user}")
        return JsonResponse(
            {
                'message': 'Two steps ahead of you. Here\'s the default settings; now stop misusing this site and get back to playing.',
                'primary': '#03A5FC',
                'secondary': '#FC0B03',
                'tertiary': '#FAD102',
                'quaternary': '#02FABC',
                'faint1': '#ABCDEF',
                'faint2': '#D6C1C1',
                'sfaint1': '#D5E6F7',
                'sfaint2': '#EBE0E0',
                'bgcolor': '#FFFFFF',
                'fbgcolor': '#AAAAAA',
                'affirm': '#639919',
                'affirm2': '#F5E911',
                'neutral': '#777777',
                'negative': 'C94040',
                'font_family': 'Helvetica',
                'font_heading': 'Helvetica',
                }
            )
    
    return JsonResponse(
        {
            'primary': user.primary_color,
            'secondary': user.secondary_color,
            'tertiary': user.tertiary_color,
            'quaternary': user.quaternary_color,
            'faint1': user.faint_primary_color,
            'faint2': user.faint_secondary_color,
            'sfaint1': user.superfaint_primary_color,
            'sfaint2': user.superfaint_secondary_color,
            'bgcolor': user.background_color,
            'fbgcolor': user.background_highlight_color,
            'affirm': user.affrm_color,
            'affirm2': user.afrm2_color,
            'neutral': user.neutral_color,
            'negative': user.negative_color,
            'font_family': user.font_family,
            'font_heading': user.heading_font,
            }
        ) # Wow, that's a lot of settings.


def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {
                'message': 'Username or password is incorrect.',
                })
        
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            return render(request, 'register.html', {
                'message': 'Confirmation does not match password.'
            })
        
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username taken.'
            })

        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:        
        return render(request, 'register.html')
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def about(request, game_tli):
    return render(request, f'about/{game_tli}.html')

def make_adw(request):
    if request.method == 'POST':
        n = int(request.POST['n'])
        
        new = Game(
            flattened = '',
            nplayers = n,
            extra_data = str(['']*n),
            ready = 0,
            game_tli = 'ADW',
            code = 0,
            completed = False,
            nmoves = 0,
            made_by = request.user,
            )
        seed = new.pk
        new.code = code(seed, 11)
        new.save()

        new_pl = Player(
            user = request.user,
            game = new,
            player_index = int(random.random() * n),
            hashed_id = 0,
            )
        seed = new_pl.pk
        new_pl.hashed_id = ndigint(seed, 18)
        new_pl.save()

        return HttpResponseRedirect(reverse('pregame', args=[new_pl.hashed_id]))

    else:
        return render(request, 'make/adw.html')

def pregame(request, code):
    player = Player.objects.filter(hashed_id=code).first()

    if (not player) or (request.user != player.user):
        return HttpResponseRedirect(reverse('index'))
    
    game = player.game

    return render(request, 'pre.html', {
        'code': player.hashed_id,
        'is_host': request.user == game.made_by,
        'n': game.nplayers,
        'gc': game.code,
        })

def get_players(request):
    player = Player.objects.filter(hashed_id=request.GET['code']).first()
    
    if (not player) or (request.user != player.user):
        warn(f"Attempt to access get-pl through {request.GET['code']} by {request.user}")
        return JsonResponse(
            {
                'message': 'TWO STEPS AHEAD.'
                }
            )
    game = player.game
    players = Player.objects.filter(game=game)
    usernames = [p.user.username for p in players]
    return JsonResponse(
        {
            'players': usernames,
            'has_begun': int(bool(game.ready)),
            'nplayers': len(usernames),
            'reqplayers': game.nplayers,
            }
        )
    
def begin(request):
    if request.method == 'POST':
        player = Player.objects.filter(hashed_id = request.POST['code']).first()
        if (not player) or (player.game.made_by != request.user):
            return HttpResponseRedirect(reverse('index'))

        players = Player.objects.filter(game = player.game)
        
        if len(players) < player.game.nplayers:
            return HttpResponseRedirect(reverse('pregame', args=[player.hashed_id]))

        player.game.ready = 1 
        player.game.save()

        return HttpResponseRedirect(reverse('play-adw', args=[player.hashed_id]))
    else:
        return HttpResponseRedirect(reverse('index'))

    

def join(request):
    if request.method == 'POST':
        code = request.POST['code']
        game = Game.objects.filter(code=code).first()

        other_pl = Player.objects.filter(game=game)
        other_users = [opp.user for opp in other_pl]
        if request.user in other_users:
            pl = other_pl.filter(user=request.user).first()
            return HttpResponseRedirect(reverse('pregame', args=[pl.hashed_id]))

        if len(other_pl) == game.nplayers:
            return render(request, 'join.html', {
                'alert_message': 'The game you attempted to join is full. If you joined with a code, ask the giver to ensure that everybody in the game is supposed to be there.'
                }
                )
        
        new_pl = Player(
            user = request.user,
            game = game,
            player_index = 0,
            hashed_id = 0,
            )

        other_ind = []
        for opp in other_pl:
            other_ind.append(opp.player_index)

        pi = 0

        while pi in other_ind:
            pi = int(random.random() * game.nplayers)

        new_pl.player_index = pi

        seed = new_pl.pk
        new_pl.hashed_id = ndigint(seed, 19)

        new_pl.save()

        

        return HttpResponseRedirect(reverse('pregame', args=[new_pl.hashed_id]))
    else:
        return render(request, 'join.html')
                          
            
def play(request, code):
    player = Player.objects.filter(hashed_id=code).first()

    if (not player) or (request.user != player.user):
        if player:
            warn(f"Attempt to access game {player.game.code}({player.hashed_id}) by {request.user.username}.")
            return HttpResponseRedirect(reverse('index'), {
                'alert_message': 'How\'d you even.. whatever. This incident has been reported.'
                })
        warn(f"Attempt to access nonexistent game code {code} by {request.user.username}.")
        return HttpResponseRedirect(reverse('index'), {
            'alert_message': 'Nonexistent game.'
            })

    game = player.game
    user = player.user

    if game.game_tli == 'ADW':
        return HttpResponseRedirect(reverse('play-adw', args=[code]))
    
def play_adw(request, code):
    player = Player.objects.filter(hashed_id=code).first()

    if (not player) or (request.user != player.user):
        if player:
            warn(f"Attempt to access game {player.game.code}({player.hashed_id}) by {request.user.username}.")
            return HttpResponseRedirect(reverse('index'), {
                'alert_message': 'How\'d you even.. whatever. This incident has been reported.'
                })
        warn(f"Attempt to access nonexistent game code {code} by {request.user.username}.")
        return HttpResponseRedirect(reverse('index'), {
            'alert_message': 'Nonexistent game.'
            })

    game = player.game
    user = player.user
    
    if request.method == 'POST':
        if game.ready == 1:
            w = request.POST['word'].lower()
            if w in GUESS:
                pw = eval(game.extra_data)
                pw[player.player_index] = w
                game.extra_data = str(pw)
                if '' not in pw:
                    game.ready = 2
                    Q = "\',\'" # This has to be done because f-strings don't let you have backslashes
                    game.flattened = str(f"['ADW', [], (\'{Q.join(pw)}\')]")
                game.save()
                return JsonResponse({
                    'accepted': True,
                    'msg': 'Move accepted.',
                })
            else:
                return JsonResponse({
                    'accepted': False,
                    'msg': '{w.upper()} is not a valid word.',
                })
        elif game.ready == 2:
            if game.flattened:
                game_obj = build_game(*eval(game.flattened))
            else:
                game_obj = build_game('ADW', [], (eval(game.extra_data),))
            print('*********~~~*~*~*~*~*~*~*HERE*~*~**~***~****~***~***')
            if player.player_index == game_obj.to_move:
                print('*********~~~*~*~*~*~*~*~*&THERE*~*~**~***~****~***~***')
                if game_obj.move(request.POST['guess']):
                    game.nmoves += 1
                    game.flattened = str(deflate_game(game_obj))
                    if (game_obj.win + 1):
                        game.completed = 1
                        
                        game.ready = 3
                    game.save()

                    return render(request, 'play/adw2.html', {
                        'code': code,
                        'R': range(game.nplayers),                        
                    })
                else:
                    return render(request, 'play/adw2.html', {
                        'message': game_obj.whywrong(request.POST['guess']),
                        'code': code,
                        'R': range(game.nplayers),                        
                    })
            else:
                return render(request, 'play/adw2.html', {
                        'message': game_obj.whywrong(request.POST['guess']),
                        'code': code,
                        'R': range(game.nplayers),                        
                    })

        elif game.ready == 3:
            return HttpResponseRedirect(reverse('winscreen', args=[code]))
                
            

    else:
        if game.ready == 1:
            pw = eval(game.extra_data)
            if pw[player.player_index] == '':
                return render(request, 'play/adw1.html')
            else:
                return render(request, 'play/adw1.html', {
                    'word': pw[player.player_index],
                    })
        
        elif game.ready == 3:
            return HttpResponseRedirect(reverse('winscreen', args=[code]))
        
        else:
            return render(request, 'play/adw2.html', {
                'R': range(game.nplayers),
                'code': code
                })
            
def get_state_adw(request):
    code = request.GET['c']
    player = Player.objects.filter(hashed_id=code).first()
    if (not player) or (request.user != player.user):
        warn(f"Attempt to access get-state-adw through {request.GET['code']} by {request.user}")
        return JsonResponse(
            {
                'message': 'I will always be two steps ahead.'
                }
            )
    game = player.game
    user = player.user
    players = Player.objects.filter(game=game)
    if game.flattened:
        print(game.flattened)
        game_obj = build_game(*eval(game.flattened))
    else:
        game_obj = build_game('ADW', [eval(game.extra_data)], [])
    return JsonResponse({
        'to_play': game_obj.to_move,
        'guess': game_obj.guesses,
        'fb': game_obj.fb,
        'n': game_obj.N,
        'w': game_obj.win,
        'users': [Player.objects.filter(game=game, player_index=i).first().user.username for i in range(game_obj.N)],
        'i': player.player_index,
        })

def winscreen(request, code):
    game = Player.objects.filter(hashed_id=code).first().game
    return render(request, 'win.html', {
            "winner": Player.objects.filter(game=game).filter(player_index=build_game(*eval(game.flattened)).win).first().user.username,
            })

