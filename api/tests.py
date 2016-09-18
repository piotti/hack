from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from api.models import CuckUser
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

		me_c = CuckUser.objects.get(user=user)
		me_c.lat_coord=0
		me_c.lon_coord=0
		me_c.save()
		
		lat='0.0'
		lon='0.0'

		u1 = User(username='u1')
		u1.save()
		p1 = CuckUser(user=u1,
			lat_coord=0,
			lon_coord=0)
		p1.save()

		u2 = User(username='u2')
		u2.save()
		p2 = CuckUser(user=u2,
			lat_coord=0,
			lon_coord=0)
		p2.save()

		u3 = User(username='u3')
		u3.save()
		p3 = CuckUser(user=u3,
			lat_coord=2,
			lon_coord=0)
		p3.save()

		u4 = User(username='u4')
		u4.save()
		p4 = CuckUser(user=u4,
			lat_coord=0,
			lon_coord=-2)
		p4.save()

		bounds = '-1,1,-1,1'

		resp = c.get('/api/ping/%s/%s/%s,%s/?bounds=%s' % (
				user.username,
				key,
				lat,
				lon,
				bounds
			)
		)


		self.assertEqual(resp.status_code, 200)
		self.assertIs(type(resp.json()['nearby_players']), list)
		self.assertEqual(len(resp.json()['nearby_players']), 2)
		




