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

decorators = [csrf_exempt, login_required]

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class WalletCreation(View):

    def post(self, request):
        data = request.POST
        try:
            username = str(request.user)
            wname = str(data.get("name"))
            amount = float(data.get("amount"))
            walletid = int((Wallet.objects.count()) + 1)
            wallet = Wallet(WalletID=walletid, name=wname, user=username, amount=amount).save()
            return JsonResponse({"created": data}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class WalletList(View):

    def get(self, request):
        try:
            username = str(request.user)
            print(username)
            wallets = Wallet.objects(user=username)
            a = []
            for w in wallets:
                a.append({
                    "name": str(w.name), "id": str(w.WalletID), "amount": str(w.amount)
                    })
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
                amount2 = float(data.get("amount"))
                wallet = Wallet._get_collection().find_and_modify(
                    query={'WalletID': walletid},
                    update={'$inc':{'amount': amount2}},
                    new=True
                )
                Transaction(transType='Charge', fwalletid=walletid, amount=amount2).save()
                return JsonResponse({"Charged": str(amount2)}, safe=False)
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
                amount2 = float(data.get("amount"))
                wallet = Wallet._get_collection().find_and_modify(
                    query={'WalletID': walletid, 'amount':{'$gte': amount2}},
                    update={'$inc':{'amount': amount2 * -1}},
                    new=True
                )
                if wallet is not None:
                    Transaction(transType='Decharge', fwalletid=walletid, amount=amount2).save()
                    return JsonResponse({"Decharged": str(amount2)}, safe=False)
                else:
                    return JsonResponse({"error": "Not sufficient value"}, safe=False)
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
            if str(request.user) == str(sourceWallet[0].user):
                amount2 = float(data.get("amount"))
                wallet = Wallet._get_collection().find_and_modify(
                    query={'WalletID': sourceWallId, 'amount':{'$gte': amount2}},
                    update={'$inc':{'amount': amount2 * -1}},
                    new=True
                )
                if wallet is not None:
                    wallet1 = Wallet._get_collection().find_and_modify(
                    query={'WalletID': destWallId},
                    update={'$inc':{'amount': amount2}},
                    new=True
                    )
                    Transaction(transType='Transfer', fwalletid=sourceWallId, swalletid=destWallId, amount=amount2).save()
                    Transaction(transType='Charge', fwalletid=destWallId, amount=amount2).save()
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

