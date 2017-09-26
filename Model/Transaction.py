import sys


class Transaction:
  payerCountry = "*"
  beneficiaryCountry = "CN"
  transactionType = "P2P"
  channel = "ICBC"
  paymentMethod = "LOCAL"
  paymentCountry = "CN"
  paymentCurrency = "CNY"

  def __init__(self, payerCountry = "*", beneficiaryCountry = "CN", transactionType = "P2P", channel = "ICBC", paymentMethod = "LOCAL", paymentCountry = "CN",
               paymentCurrency = "CNY"):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    self.payerCountry = payerCountry
    self.beneficiaryCountry = beneficiaryCountry
    self.transactionType = transactionType
    self.channel = channel
    self.paymentMethod = paymentMethod
    self.paymentCountry = paymentCountry
    self.paymentCurrency = paymentCurrency

  def toString(self):
    return "Transaction: payerCountry is " + self.payerCountry + ", beneficiaryCountry is " + self.beneficiaryCountry + ", transactionType is " + self.transactionType + ", channel is " + self.channel + ", paymentMethod is " + self.paymentMethod + ", paymentCountry is " + self.paymentCountry + ", paymentCurrency is " + self.paymentCurrency
