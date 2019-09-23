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
import requests as req

CLIENT_ID = '123456'
CLIENT_SECRET = '123456'


@method_decorator(csrf_exempt, name='dispatch')
class UserRegister(View):

    def post(self, request):
        data = request.POST
        try:
            user = User.objects.create_user(username=data.get("username"), email=data.get("email"), password=data.get("password"))
            return JsonResponse({"created": data}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(View):
    
    def post(self, request):
        data = request.POST
        try:
            use = data.get("username")
            passwd = data.get("password")
            email = data.get("email")
            user = auth.authenticate(username=use, password=passwd)
            if user is not None:
                auth.login(request, user)
                r = req.post('http://127.0.0.1:8000/o/token/',
                    data={
                        'grant_type': 'password',
                        'username': data.get("username"),
                        'password': data.get("password"),
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET,
                        'redirect_uri': 'http:example.com/'
                    },
                )
                a = r.content.decode()
                return HttpResponse(a)

        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)
