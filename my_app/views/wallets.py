from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import auth
import json
from my_app.models import Wallet, Transaction
import mongoengine
import itertools
import requests as req

decorators = [csrf_exempt, login_required]

@method_decorator(decorators, name='dispatch')
class WalletCreation(View):
    
    def post(self, request):
        data = request.POST
        print(data)
        try:
            username = str(request.user)
            wname = str(data.get("name"))
            amount = float(data.get("amount"))
            walletid = int((Wallet.objects.count()) + 1)
            print(walletid)
            wallet = Wallet(WalletID=walletid, name=wname, user=username, amount=amount).save()
            print(wallet)
            return JsonResponse({"created": data}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)


@method_decorator(decorators, name='dispatch')
class WalletList(View):

    def get(self, request):
        try:
            username = str(request.user)
            wallet = Wallet.objects(user=username)
            a = {}
            for w, i in itertools.product(wallet, range(len(wallet))):
                a[str(i)] = [{"name": str(w.name), "id": str(w.WalletID), "amount": str(w.amount)}]
            return JsonResponse(a, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)

@method_decorator(decorators, name='dispatch')
class WalletId(View):

    def get(self, request, wallid):
        try:
            wallet = Wallet.objects(WalletID=wallid)
            if str(request.user) == wallet[0].user:
                a = {"name": str(wallet[0].name), "Amount": str(wallet[0].amount)}
                return JsonResponse(a, safe=False)
            else:
                return JsonResponse({"error": "not allowed"}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)

@method_decorator(decorators, name='dispatch')
class ChargeWallet(View):

    def post(self, request):
        data = request.POST
        try:
            walletid = int(data.get("id"))
            wallet = Wallet.objects(WalletID=walletid)
            if str(request.user) == str(wallet[0].user):
                amount1 = float(wallet[0].amount)
                amount2 = float(data.get("amount"))
                amountFinal = amount1 + amount2
                wallet.update(amount=amountFinal)
                wallet[0].save()
                Transaction(transType='Charge', fwalletid=walletid, amount=amountFinal).save()
                return JsonResponse({"Charged": str(amountFinal)}, safe=False)
            else:
                return JsonResponse({"error": "Not allowed"}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)



@method_decorator(decorators, name='dispatch')
class DechargeWallet(View):

    def post(self, request):
        data = request.POST
        try:
            walletid = int(data.get("id"))
            wallet = Wallet.objects(WalletID=walletid)
            if str(request.user) == str(wallet[0].user):
                amount1 = float(wallet[0].amount)
                amount2 = float(data.get("amount"))
                amountFinal = amount1 - amount2
                if amountFinal >= 0:
                    wallet.update(amount=amountFinal)
                    wallet[0].save()
                    Transaction(transType='Decharge', fwalletid=walletid, amount=amountFinal).save()
                    return JsonResponse({"Decharged": str(amountFinal)}, safe=False)
                else:
                    return JsonResponse({"error": "Not enough value"}, safe=False)
            else:
                return JsonResponse({"error": "Not allowed"}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)

@method_decorator(decorators, name='dispatch')
class Transfer(View):

    def post(self, request):
        data = request.POST
        try:
            sourceWallId = int(data.get("Sourceid"))
            destWallId = int(data.get("Destid"))
            sourceWallet = Wallet.objects(WalletID=sourceWallId)
            destWallet = Wallet.objects(WalletID=destWallId)
            if str(request.user) == str(sourceWallet[0].user):
                amount1 = float(sourceWallet[0].amount)
                amount2 = float(data.get("amount"))
                sourceAmountFinal = amount1 - amount2
                amount1 = float(destWallet[0].amount)
                destAmountFinal = amount1 + amount2
                if sourceAmountFinal >= 0:
                    destWallet.update(amount=destAmountFinal)
                    sourceWallet.update(amount=sourceAmountFinal)
                    destWallet[0].save()
                    sourceWallet[0].save()
                    Transaction(transType='Transfer', fwalletid=sourceWallId, swalletid=destWallId, amount=amount2).save()
                    return JsonResponse({"Transfered": str(amount2)}, safe=False)
                else:
                    return JsonResponse({"error": "Not enough value"}, safe=False)
            else:
                return JsonResponse({"error": "Not allowed"}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)


@method_decorator(decorators, name='dispatch')
class WalletTransactions(View):
    def get(self, request, wallid):
        try:
            wa = Wallet.objects(WalletID=wallid)
            print(str(request.user))
            print(str(wa[0].user))
            if str(request.user) == str(wa[0].user):
                print("abbas")
                page = int(request.GET.get('page'))
                tr = Transaction.objects(fwalletid=wallid)
                p = Paginator(tr, page)
                paglist = []
                pagdict = {}
                for i in range(p.num_pages):
                    for j in range(len(p.page(i+1))):
                        paglist.append({"type":str(p.page(i+1).object_list[j].transType), "amount":str(p.page(i+1).object_list[j].amount)})
                    pagdict[str(i+1)] = paglist
                    paglist = []
                return JsonResponse(pagdict, safe=False)
            else:
                return JsonResponse({"error": "Not allowed"}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)



