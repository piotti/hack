from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#from .models import *
# Create your tests here.

class ApiTests(TestCase):

	def makeTestUser(self, c):
		c.get('/api/create_user/?username=test1&password=test1')
		resp = c.get('/api/login_user/?username=test1&password=test1').json()
		user = User.objects.get(username='test1')
		return (user, resp['auth_key'])

	def test_ping(self):
		c = Client()

		user, key = self.makeTestUser(c)
		
		lat='0'
		lon='0'

		bounds = '-1,1,-1,1'

		resp = c.get('/ping/%s/%s/%s,%s/?bounds=%s' % (
				user.username,
				key,
				lat,
				lon,
				bounds
			)
		)

		self.assertEqual(resp.status_code, 200)
		self.assertIs(type(resp['nearby_players']), type(list))
		




