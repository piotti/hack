from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CuckUser(models.Model):

	user = models.OneToOneField(User, related_name='cuck_user')
	lat_coord = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
	lon_coord = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
	money = models.IntegerField(default=100)

	session_auth = models.CharField(max_length=64, blank=True)


	def serialize(self):
		#Returns JSON of position for other players to access
		return {
			'lat_coord':self.lat_coord,
			'lon_coord':self.lon_coord,
		}

	def serializeProfile(self):
		return {
			'name':self.user.username,

		}

	def __str__(self):
		return self.user.username


