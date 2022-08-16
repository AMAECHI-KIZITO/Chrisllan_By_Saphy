from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from chrysllan_pkg import config
app=Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config.from_object(config.LiveConfig)
csrf=CSRFProtect(app)
db=SQLAlchemy(app)
from chrysllan_pkg.routes import user_route,admin_route
from chrysllan_pkg import models