from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
from flask_login import login_required, LoginManager, login_user
from core_service import Parser
from Model.Transaction import Transaction
from Model.user import User, db
from flask_redis import FlaskRedis
import cPickle as pickle
import redis


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@my_postgres/postgres'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost/postgres'
app.config['REDIS_URL'] = "redis://:@my_redis:6379/"
#app.config['REDIS_URL'] = "redis://:@localhost:6379/"
db.init_app(app)
with app.app_context():
  db.create_all()
  db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

redis_store = FlaskRedis(app)

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

    transKey = pickle.dumps(transaction)
    search_type = request.form.get('type')
    isRedisAlive = True
    try:
      llen = redis_store.llen(transKey)
    except redis.exceptions.ConnectionError as e:
      isRedisAlive = False
      print "Redis service dead!"

    if isRedisAlive:
      if llen == 0 :
        parser.setTransaction(transaction)
        required_fields = parser.dumpRequiredFields()
        payloads = parser.generateTest()
        requiredFieldsValue = pickle.dumps(required_fields)
        payloadsValue = pickle.dumps(payloads)

        redis_store.rpush(transKey,requiredFieldsValue, payloadsValue)

        if search_type == 'field':
          print required_fields
          return render_template("result_fields.html", required_fields=required_fields)
        else:
          print payloads
          return render_template("result_payloads.html", payloads=payloads)
      else:
        requiredFieldsValue = redis_store.lindex(transKey, 0)
        payloadsValue = redis_store.lindex(transKey, 1)
        required_fields = pickle.loads(requiredFieldsValue)
        payloads = pickle.loads(payloadsValue)
        if search_type == 'field':
          return render_template("result_fields.html", required_fields=required_fields)
        else:
          return render_template("result_payloads.html", payloads=payloads)

    else:
      parser.setTransaction(transaction)
      required_fields = parser.dumpRequiredFields()
      payloads = parser.generateTest()
      if search_type == 'field':
        return render_template("result_fields.html", required_fields=required_fields)
      else:
        return render_template("result_payloads.html", payloads=payloads)

if __name__ == '__main__':
	#print jdata
  app.secret_key = 'Airwallex'
  app.run(debug=True, host='0.0.0.0')