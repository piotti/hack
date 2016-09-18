from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from . import login_views

'''
def ping_location(request, lat, lon):
	pass
'''


from .logic import person #Austin's shit here

from .models import *

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

	me_c = get_player_from_username(username)
	me_c.lat_coord = lat
	me_c.lon_coord = lon
	me_c.save(update_fields=['lat_coord', 'lon_coord'])
	notifs = [n.msg for n in list(me_c.notifications.all())]
	me_c.notifications.clear()

	return JsonResponse({
		'nearby_players':[p.serialize() for p in players if p != me_c],
		'notifications':notifs
		})


def player_info(request, username, auth, player_name):
	if not login_views.authenticate(username, auth):
		return auth_error()

	player = get_player_from_username(player_name)

	c = player.serializeProfile()
	

	if player_name == username:
		#More information for own profile
		c['money'] = player.money

	return JsonResponse(c)






### ACTIONS ###

def mug(request, username, auth, player_name):
	if not login_views.authenticate(username, auth):
		return auth_error()

	def error(msg):
		return JsonResponse({
		'success':False,
		'message': msg,
		'transaction':0,
		'your_money':player1.money,

		})

	player1 = get_player_from_username(username)
	player2 = get_player_from_username(player_name)

	if player1.mugger_set.all().count() != 0 and player1.muggee_set.all().count() != 0:

		last_mug_date = max(
			player1.mugger_set.filter(muggee=player2).order_by('-date')[0].date,
			player1.muggee_set.filter(mugger=player2).order_by('-date')[0].date
			)

		if last_mug_date > timezone.now() - datetime.timedelta(0, 180):
			return error('You mugged or got mugged by this person too recently')
	

	mugData = person.mug(player1, player2)

	success = mugData['amount'] > 0
	msg = mugData['reason']

	if success:
		mugging = Mugging(mugger=player1, muggee=player2, date=timezone.now())
		mugging.save()

	player2.sendNotification('mug')

	return JsonResponse({
		'success':success,
		'message': msg,
		'transaction':mugData['amount'],
		'your_money':player1.money,

		})


def bust(request, username, auth, player_name):
	pass
		




