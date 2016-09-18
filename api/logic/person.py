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





def mug(mugger, muggee): #mugger_score, muggee_score):
	"""
	mugger: Person object
	muggee: Person object
	"""
	return_dict = {}

	p1_coords = (mugger.lat_coord, mugger.lon_coord)
	p2_coords = (muggee.lat_coord, muggee.lon_coord)

	mug_limit = 20

	distance = get_distance_length(p1_coords,p2_coords)
	assert type(distance) = tuple, "Distance:", distance

	if distance < mug_limit:
		effectiveness = 1 - distance/mug_limit
		money_transferred = int(effectiveness * (muggee.money) / (muggee.money + 1) ** 0.5)
		assert money_transferred > 0, "Transaction size: %r" % money_transferred ####

		if muggee.money < 0:
			return_dict["amount"] = 0
			return_dict["reason"] = "Muggee is broke"


		mugger.money += money_transferred

		if muggee.money < money_transferred:
			mugee.money = 0
		else:
			muggee.money -= money_transferred

		mugger.reputation += 1
		mugger.suspicion += 1

		mugger.save(update_fields=["money", "reputation", "suspicion"])
		muggee.save(update_fields=["money"])

		return_dict["amount"] = money_transferred
		return_dict["reason"] = "none"

	else:
		return_dict["amount"] = 0
		return_dict["reason"] = "Target too far"


	return return_dict


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

def drug_deal(dealer, customer, drug_amount):
	"""
	dealer: Person object
	customer: Person object

	"""
	assert drug_amount > 0, "Drug amount: %r" % drug_amount ####
	return_dict = {}
	if (date.datetime.utcnow() - dealer.last_drug_transaction) > date.datetime(0, 0, 0, 0, 0, 1):
		if (date.datetime.utcnow() - customer.last_drug_transaction) > date.datetime(0, 0, 0, 0, 0, 1):
			drug_price = (drug_amount) ** (2/3)

			money_amount = int(drug_amount * drug_price)

			if customer.money < money_amount:
				return_dict["money_amount"] = 0
				return_dict["reason"] = "Customer has insufficient money"

			dealer.money -= money_amount
			customer.money += money_amount

			dealer.drugs += drug_amount
			customer.drugs -= drug_amount

			dealer.last_drug_transaction = datetime.datetime.utcnow()
			customer.last_drug_transaction = datetime.datetime.utcnow()

			dealer.suspicion += 1
			customer.suspicion += 1

			dealer.save(update_fields=["money", "drugs", "last_drug_transaction", "suspicion"])
			customer.save(update_fields=["money", "drugs", "last_drug_transaction", "suspicion"])

			return_dict["money_amount"] = money_amount
			return_dict["reason"] = "none"
		else:
			return_dict["money_amount"] = 0
			return_dict["reason"] = "customer is making too many transactions"
	else:
		return_dict["money_amount"] = 0
		return_dict["reason"] = "dealer is making too many transactions"

	return return_dict


def buy_in_bulk(player, drug_amount):
	"""
	Buy drugs in bulk from Pepe Escobal
	"""
	assert drug_amount > 0, "Drug amount: %r" % drug_amount ####

	return_dict = {}
	if (date.datetime.utcnow() - player.last_drug_transaction) > date.datetime(0, 0, 0, 0, 0, 1):
		if drug_amount >= 1000:
			drug_price = (drug_amount)**(2/3)
			money_amount = int(drug_amount * drug_price)

			if player.money < money_amount:
				return_dict["money_amount"] = 0
				return_dict["reason"] = "Customer has insufficient money"

			player.money -= money_amount
			player.drugs += drug_amount
			player.last_drug_transaction = datetime.datetime.utcnow()

			player.save(update_fields=["money", "drugs", "last_drug_transaction"])

			return_dict["money_amount"] = money_amount
			return_dict["reason"] = "none"
		else:
			return_dict["money_amount"] = 0
			return_dict["reason"] = "Insufficient drugs requested"
	else:
		return_dict["money_amount"] = 0
		return_dict["reason"] = "customer is making too many transactions"

	return return_dict


def sell_to_pleb(player):
	"""
	Sell drugs to bot
	Can only sell in single units
	"""
	return_dict = {}
	if (date.datetime.utcnow() - player1.last_drug_transaction) > date.datetime(0, 0, 0, 0, 0, 30):
		player.money += 1
		player.drugs -= 1
		player.last_drug_transaction = datetime.datetime.utcnow()

		player.save(update_fields=["money", "drugs", "last_drug_transaction"])

		return_dict["money_amount"] = money_amount
		return_dict["reason"] = "none"
	else:
		return_dict["money_amount"] = 0
		return_dict["reason"] = "dealer is making too many transactions"

	return return_dict


def bust(rat, victim):
	"""
	rat: person
	victim: person
	rat causes victim to be busted
	victim loses all drugs
	Reputation is the number of times the victim mugged someone without getting caught
	Reputation reset to zero
	Rat gets commission equal to 2 ^ reputation of victim
	"""

	victim.drugs = 0

	rat.money += 2 ** victim.reputation

	victim.reputation = 0

	rat.suspicion -= 5
	victim.suspicion += 2

	victim.save(update_fields=["drugs", "reputation", "suspicion"])
	rat.save(update_fields=["money", "suspicion"])
