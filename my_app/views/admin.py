from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import json
from my_app.models import Wallet, Transaction
import mongoengine
import itertools

decorators = [csrf_exempt, login_required]



