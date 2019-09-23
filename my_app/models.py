from mongoengine import *
import datetime

class Wallet(Document):
    WalletID = IntField(min_value=1)
    name = StringField(max_length=20)
    user = StringField(max_length=50)
    amount = DecimalField(min_value=0)

class Transaction(Document):
    typeChoice = ('Charge', 'Decharge', 'Transfer')
    date = DateTimeField(default=datetime.datetime.now())
    transType = StringField(max_length=8, choices=typeChoice)
    fwalletid = IntField()
    swalletid = IntField(default=None)
    amount = DecimalField(min_value=0)
    