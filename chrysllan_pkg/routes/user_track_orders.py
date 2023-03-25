import requests, json
from datetime import date
from flask import render_template, session, redirect
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *


# Track Order View
@app.route('/track-orders/')
def track_orders():
    if session.get('user_id') !=None and session.get('username') != None:
        todaysdate=date.today()
        shopping_ID = session.get('user_cart_id')
        
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        
        #getting the customer order history
        order_history=db.session.query(Order).filter(Order.buyer==session.get('user_id')).order_by(Order.order_date.desc()).all()
        
        if deetscart != []:
            total=0
            for i in deetscart:
                total=total+i.amount
            return render_template('user/trackorders.html', usercart=usercart, cartdeets=deetscart, total=total, order_history=order_history, year=date.today().year)
        else:
            total=0
            return render_template('user/trackorders.html', usercart=usercart, cartdeets=deetscart, total=total, order_history=order_history, year=date.today().year)
    else:
        return redirect('/customer/login/')
    
# customer order details
@app.route('/customer/orderdetails/<id>')
def customer_order_details(id):
    if session.get('user_id') !=None and session.get('username') != None:
        todaysdate=date.today()
        shopping_ID = session.get('user_cart_id')
        
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        
        
        order_deets=db.session.query(Order_details).filter(Order_details.order_id==id).all()
        
        order=db.session.query(Order).filter(Order.order_id==id).first()
        
        if deetscart != []:
            total=0
            for i in deetscart:
                total=total+i.amount
            return render_template('user/trackorderdetails.html', usercart=usercart, cartdeets=deetscart, total=total, order_deets=order_deets, order=order,year=date.today().year)
        else:
            total=0
            return render_template('user/trackorderdetails.html', usercart=usercart, cartdeets=deetscart, total=total, order_deets=order_deets, order=order,year=date.today().year)
    else:
        return redirect('/customer/login/')