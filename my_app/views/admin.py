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

@method_decorator(decorators, name='dispatch')
class WalletAdmin(View):
    def get(self, request):
        try:
            if request.user.is_superuser:
                newlist = []
                wlist = []
                types = ['Charge', 'Decharge', 'Transfer']
                for i in types:
                    pipline = [{"$match":{"transType": i}}, {"$group": {"_id": "$fwalletid", i: {"$sum": "$amount"}}}]
                    tr = Transaction.objects().aggregate(*pipline)
                    tr = list(tr)
                    newlist = newlist + tr
                wa = Wallet.objects()
                for a in wa:
                    wlist.append({"name": str(a.name), "_id": a.WalletID, "user": str(a.user)})
                for ta in wlist:
                    for tb in newlist:
                        if ta['_id'] == tb['_id']:
                            ta.update(tb)
                return JsonResponse(wlist, safe=False)
            else:
                return JsonResponse({"error": "not allowed"}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)

