"""
Attributes:
X coord (float)
Y coord (float)
Money
social class (string)
	classes
items
attacks

Functions:
return vicinity (square)
circle the squre


"""

from geopy.distance import vincenty
import random
import datetime

earth_radius = 6.371*10**6

def get_distance_length(coord1, coord2):
	return vincenty(coord1, coord2).m

def get_square_range(lat, lon):
	"""
	lat = latitude
	lon = longitude
	radius = range radius (1/2 length of range width)
	returns (x lower bound, x upper bound, y lower bound, y uppper bound)
	"""

	lat_lower = lat - radius
	lat_upper = lat + radius
	lon_lower = lon - radius
	lon_upper = lon + radius

	return [lat_lower, lat_upper, lon_lower, lon_upper]

def in_circle_from_square(coordinates, x, y):
	"""
	lat = range center latitude
	lon = range center longitude
	returns: list of indices of coordinates list that are in circle
	"""
	assert type(coordinates) is list, "Data supplied is not in list"

	ind_circle = []
	coords_normalized = []
	for i in coordinates:
		lat_norm = i[0] - lat
		lon_norm = i[1] - lon
		coords_normalized.append([x_norm, y_norm])

	for x in xrange(len(coords_normalized)):
		distance = (coords_normalized[x][0]**2 + coords_normalized[x][1]**2)**0.5
		if distance > radius:
			ind_circle.append(x)

	return ind_circle





def mug(player1, player2): #mugger_score, muggee_score):
	"""
	player1: Player 1 object (mugger)
	player2: Player 2 object (muggee)
	"""

	p1_coords = (player1.lat_coord, player1.lon_coord)
	p2_coords = (player2.lat_coord, player2.lon_coord)

	mug_limit = 20

	distance = get_distance_length(p1_coords,p2_coords)

	if distance < mug_limit:
		effectiveness = 1 - distance/mug_limit
		money_transferred = int(effectiveness * (player2.money) / (player2.money + 1) ** 0.5)
		player1.money += money_transferred
		player2.money -= money_transferred

		player1.save(update_fields=["money"])
		player2.save(update_fields=["money"])


def money_transfer(player1, player2, amount):
	"""
	player1: Player 1 object (transferrer)
	player2: Player 2 object (transferee)
	"""
	amount = int(amount)
	player1.money -= amount
	player2.money += amount

	player1.save(update_fields=["money"])
	player2.save(update_fields=["money"])


def drug_deal(player1, player2, drug_amount):
	"""
	player1: Player 1 object (dealer)
	player2: Player 2 object (customer)

	"""
	if (date.datetime.utcnow() - player1.last_drug_transaction) > date.datetime(0, 0, 0, 0, 0, 30):

		drug_price = (drug_amount) ** (2/3)

		money_amount = int(drug_amount * drug_price)
		player1.money -= money_amount
		player2.money += money_amount

		player1.drugs += drug_amount
		player2.drugs -= drug_amount

		player1.last_drug_transaction = datetime.datetime.utcnow()
		player2.last_drug_transaction = datetime.datetime.utcnow()

		player1.save(update_fields=["money", "drugs", "last_drug_transaction"])
		player2.save(update_fields=["money", "drugs", "last_drug_transaction"])


def buy_in_bulk(player, drug_amount):
	"""
	Buy drugs in bulk from Pepe Escobal
	"""
	if (date.datetime.utcnow() - player1.last_drug_transaction) > date.datetime(0, 0, 0, 0, 0, 30):
		if drug_amount >= 1000:
			drug_price = (drug_amount)**(2/3)

			money_amount = int(drug_amount * drug_price)
			player.money -= money_amount

			player.drugs += drug_amount

			player.last_drug_transaction = datetime.datetime.utcnow()

			player.save(update_fields=["money", "drugs", "last_drug_transaction"])


def sell_to_pleb(player):
	"""
	Sell drugs to bot
	Can only sell in single units
	"""
	if (date.datetime.utcnow() - player1.last_drug_transaction) > date.datetime(0, 0, 0, 0, 0, 30):

		player.money += 1

		player.drugs -= 1

		player.last_drug_transaction = datetime.datetime.utcnow()

		player.save(update_fields=["money", "drugs", "last_drug_transaction"])