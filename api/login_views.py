from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.utils import IntegrityError
from django.contrib import auth

from .models import *

import random, string


# Create your views here.

def generate_key(n):
	return ''.join(random.choice(string.ascii_uppercase +string.ascii_lowercase + string.digits) for _ in range(n))

def authenticate(username, key):
	if username == '' or key == '':
		return False
	try:
		cuck_user = User.objects.get(username=username).cuck_user
	except Exception:
		return False
	return cuck_user.session_auth == key

def index(request):
	return render(request, 'api/index.html', {})

def create_user(request):
	def error(msg):
		return JsonResponse({'succes':False, 'error':msg})
	username = request.GET.get('username', '')
	password = request.GET.get('password', '')
	if username == '' or password == '':
		return error('bad username/password')

	try:
		User.objects.create_user(username, password=password)
		user = User.objects.get(username=username)
		cuckuser = CuckUser(user=user)
		cuckuser.save()
	except IntegrityError:
		return error('user already exists')

	return JsonResponse({'succes':True})

def login_user(request):
	username = request.GET.get('username', '')
	password = request.GET.get('password', '')

	user = auth.authenticate(username=username, password=password)
	if user is not None:
		auth.login(request, user)
		cuckuser = user.cuck_user
		session_auth = generate_key(32)
		cuckuser.session_auth = session_auth
		cuckuser.save()

		return JsonResponse({'success':True, 'auth_key':session_auth})
	else:
		return JsonResponse({'success':False})

