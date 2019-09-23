from django.urls import path
from . import views
from my_app.views.users import UserLogin, UserRegister
from my_app.views.wallets import WalletCreation, WalletList, WalletId, ChargeWallet, DechargeWallet, Transfer

urlpatterns = [
    path('user/register/', UserRegister.as_view()),
    path('user/login/', UserLogin.as_view()),
    path('wallet/create/', WalletCreation.as_view()),
    path('wallet/list/', WalletList.as_view()),
    path('wallet/<int:wallid>/', WalletId.as_view()),
    path('wallet/charge/', ChargeWallet.as_view()),
    path('wallet/decharge/', DechargeWallet.as_view()),
    path('wallet/transfer/', Transfer.as_view()),
]