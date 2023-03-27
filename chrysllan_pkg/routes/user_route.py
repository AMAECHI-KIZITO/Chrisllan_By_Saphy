from datetime import date
from flask import render_template, session, request
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

## Home Page Route
@app.route('/')
def home():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID == None:
        user_ip = str(request.environ.get('HTTP_X_FORWARDED_FOR', request.environ['REMOTE_ADDR']))
        split_address = user_ip.split('.')
        formatted_ip = int(''.join(split_address))
        
        session['user_cart_id'] = formatted_ip
        shopping_ID = session.get('user_cart_id')
        
        todaysdate=date.today()
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
            return render_template('user/index.html',usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)
        else:
            total=0        
            return render_template('user/index.html',usercart=usercart,cartdeets=deetscart,total=total, year=date.today().year)
    else:
        shopping_ID = session.get('user_cart_id')
        todaysdate=date.today()
        
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
            return render_template('user/index.html', usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)
        else:
            total=0        
            return render_template('user/index.html', usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)
