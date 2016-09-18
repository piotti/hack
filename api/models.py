from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.


class CuckUser(models.Model):

	user = models.OneToOneField(User, related_name='cuck_user')
	lat_coord = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
	lon_coord = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
	money = models.IntegerField(default=100)

	reputation = models.IntegerField(default=0)

	drugs = models.FloatField(default=0)
	last_drug_transaction = models.DateTimeField(blank=True, null=True)


	session_auth = models.CharField(max_length=64, blank=True)


	def is_criminal(self):
		if self.mugger_set.count() == 0:
			return False
		return timezone.now() - self.mugger_set.all().order_by('-date')[0].date < datetime.timedelta(0,180)

	def serialize(self):
		#Returns JSON of position for other players to access
		return {
			'lat_coord':self.lat_coord,
			'lon_coord':self.lon_coord,
			'criminal':self.is_criminal(),
		}

	def serializeProfile(self):
		d = {
			'name':self.user.username,
			'criminal':self.is_criminal(),

		}
		return d

	def __str__(self):
		return self.user.username


class Event(models.Model):
	class Meta:
		abstract=True

	date = models.DateTimeField()


class Mugging(Event):
	mugger = models.ForeignKey('CuckUser', related_name='mugger_set')
	muggee = models.ForeignKey('CuckUser', related_name='muggee_set')

	narc = models.ForeignKey('CuckUser', related_name='narc_set', default=None,blank=True)




