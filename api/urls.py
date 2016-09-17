from django.conf.urls import url, include

from . import login_views, game_views

app_name = 'api'
urlpatterns = [
	### LOGIN VIEWS ###
    url(r'^$', login_views.index, name='index'),
    url(r'^create_user/$', login_views.create_user, name='create_user'),
    url(r'^login_user/$', login_views.login_user, name='authenticate_user'),

    ### GAME VIEWS ###
    url(r'^ping/(?P<username>\w+)/(?P<auth>\w+)/(?P<lat>\d+\.\d+),(?P<lon>\d+\.\d+)/$', game_views.ping, name='ping_location'),
	url(r'^player_info/(?P<username>\w+)/(?P<auth>\w+)/(?P<player_name>\w+)/$', game_views.player_info, name='player_info'),
	

	### ACTIONS ###
	url(r'^action/mug/(?P<username>\w+)/(?P<auth>\w+)/(?P<player_name>\w+)', game_views.mug, name='mug'),

]
