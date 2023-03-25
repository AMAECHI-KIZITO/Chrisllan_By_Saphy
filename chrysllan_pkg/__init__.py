from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from chrysllan_pkg import config
app=Flask(__name__,instance_relative_config=True)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'konkakira1960@gmail.com'
app.config['MAIL_PASSWORD'] = 'sscewykbsxnfhqhv'
app.config['MAIL_USE_SSL'] = True
app.config['TESTING'] = False
app.config['MAIL_SUPPRESS_SEND '] = False
mail=Mail(app)
app.config.from_pyfile('config.py')
app.config.from_object(config.LiveConfig)
csrf=CSRFProtect(app)
db=SQLAlchemy(app)
from chrysllan_pkg.routes import user_route, admin_route, contact_us, error_handlers, newsletter, shop_pages, user_accounts, user_cart, user_login, user_order_payment, user_forgot_pswd, user_track_orders
from chrysllan_pkg import models