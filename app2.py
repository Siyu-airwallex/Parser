from flask import Flask, render_template
from Model.table_form import TransactionForm, GroupForm
from core_service import Parser


app = Flask(__name__)

@app.route('/search/required_fields', methods=['GET', 'POST'])
def search_required_fields():
  parser = Parser()
  groupform = GroupForm()
  groupform.title.data = "My Transactions"  # change the field's data
  for trans, fields in parser.dumpRequiredFields():
    transaction_form = TransactionForm()
    transaction_form.payerCountry = trans.payerCountry  # These fields don't use 'data'
    transaction_form.beneficiaryCountry = trans.beneficiaryCountry
    transaction_form.transactionType = trans.transactionType
    transaction_form.channel = trans.channel
    transaction_form.paymentMethod = trans.paymentMethod
    transaction_form.paymentCountry = trans.paymentCountry
    transaction_form.paymentCurrency = trans.paymentCurrency

    groupform.transactionmembers.append_entry(transaction_form)

  return render_template('edit-team.html', groupform=groupform)


if __name__ == '__main__':
  app.run(debug=True)
