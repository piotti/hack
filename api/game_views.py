from django.http import JsonResponse
from django.contrib.auth.models import User

from . import login_views

'''
def ping_location(request, lat, lon):
	pass
'''


from .logic import person #Austin's shit here

from .models import CuckUser

def auth_error():
	return JsonResponse({'success':False, 'error':'Authentication failed'})
def error(msg):
	return JsonResponse({'success':False, 'error':msg})

def get_player_from_username(username):
	return CuckUser.objects.get(user=User.objects.get(username=username))



def ping(request, username, auth, lat, lon):
	if not login_views.authenticate(username, auth):
		return auth_error()

	# Get bounds of square for nearby players
	bounds = [float(b) for b in request.GET.get('bounds',[]).split(',')]
	if len(bounds) != 4:
		return error('incorrect arguments--'+str(bounds))

	# Find players in that region
	players = list(CuckUser.objects.filter(
		lat_coord__gte=bounds[0],
		lat_coord__lte=bounds[1],
		lon_coord__gte=bounds[2],
		lon_coord__lte=bounds[3],
	))

	return JsonResponse({
		'nearby_players':[p.serialize() for p in players]
		})


def player_info(request, username, auth, player_name):
	if not login_views.authenticate(username, auth):
		return auth_error()

	player = get_player_from_username(player_name)

	c = {
		player.serializeProfile()
	}

	if player_name == username:
		#More information for own profile
		c['money'] = player.money

	return JsonResponse())






### ACTIONS ###

def mug(request, username, auth, player_name):
	if not login_views.authenticate(username, auth):
		return auth_error()

	player1 = get_player_from_username(username)
	player2 = get_player_from_username(player_name)

	mugSuccess = person.mug(player1, player2)

	return JsonResponse({
		'success':True,
		'your_money':player1.money,
		'their_money':player2.money

		})
		




