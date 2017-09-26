from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
from flask_login import login_required, LoginManager, login_user
from core_service import Parser
from Model.Transaction import Transaction
from Model.user import User, db


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@my_postgres/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost/postgres'
db.init_app(app)
with app.app_context():
  db.create_all()
  db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


parser = Parser(Transaction())


@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('signup.html')

  email = request.form.get('email')
  username = request.form.get('username')
  password = request.form.get('password')
  user = User(username=username, password=password, email=email)
  db.session.add(user)
  db.session.commit()
  flash("User successfully registered")
  return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')

  username = request.form.get('username')
  password = request.form.get('password')
  print 'login username: ' + username
  print 'login password: ' + password
  registered_user = User.query.filter_by(username=username, password=password).first()
  print registered_user
  if registered_user is None:
    flash('Username or Password is invalid', 'error')
    return redirect(url_for('login'))
  else:
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(url_for('query'))



@app.route('/query')
@login_required
def query():
  return render_template('query.html')


@app.route('/result', methods = ['POST','GET'])
@login_required
def result():
  if request.method == 'POST':
    payerCountry = request.form.get('payer_country')
    beneficiaryCountry = request.form.get('beneficiary_country')
    transactionType = request.form.get('transaction_type')
    channel = request.form.get('channel')
    paymentMethod = request.form.get('payment_method')
    paymentCountry = request.form.get('payment_country')
    paymentCurrency = request.form.get('payment_currency')

    print 'payerCountry' + payerCountry
    print 'beneficiaryCountry' + beneficiaryCountry
    print 'transactionType' + transactionType
    print 'channel' + channel
    print 'paymentMethod' + paymentMethod
    print 'paymentCountry' + paymentCountry
    print 'paymentCurrency'+ paymentCurrency

    transaction = Transaction(payerCountry,beneficiaryCountry, transactionType, channel, paymentMethod, paymentCountry, paymentCurrency)
    parser.setTransaction(transaction)

    search_type = request.form.get('type')
    if search_type == 'field':
      required_fields = parser.dumpRequiredFields()
      print required_fields
      return render_template("result_fields.html", required_fields=required_fields)
    else:
      payloads = parser.generateTest()
      print payloads
      return render_template("result_payloads.html", payloads=payloads)


# @app.route('/testdb', methods = ['POST','GET'])
# def testdb():
#   admin = User('charlie', "password")
#   guest = User('stefanie', "password")
#   with app.app_context():
#     db.create_all()
#   db.session.add(admin)
#   db.session.add(guest)
#
#   db.session.commit()
#   results = User.query.all()
#
#   jsonl_results = []
#   for result in results:
#     d = {'username': result.username,
#          'password': result.password}
#     jsonl_results.append(d)
#
#   return jsonify(items=jsonl_results)



if __name__ == '__main__':
	#print jdata
  app.secret_key = 'Airwallex'
  app.run(debug=True, host='0.0.0.0')