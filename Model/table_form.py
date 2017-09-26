from wtforms import Form
from wtforms import StringField
from wtforms import FieldList
from wtforms import FormField

class TransactionForm(Form):
  payerCountry = StringField('payer country')
  beneficiaryCountry = StringField('beneficiary country')
  transactionType = StringField('transaction type')
  channel = StringField('channel')
  paymentMethod = StringField('payment method')
  paymentCountry = StringField('payment country')
  paymentCurrency = StringField('payment currency')




class GroupForm(Form):
  title = StringField('title')
  transactionmembers = FieldList(FormField(TransactionForm))