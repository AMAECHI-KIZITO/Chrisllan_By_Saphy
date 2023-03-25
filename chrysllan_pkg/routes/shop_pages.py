from datetime import date
from flask import render_template, session, redirect
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

     
## Men Footware Shopping Page
@app.route('/shop/men/')
def shop_men():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        todaysdate=date.today()
        men_footware=db.session.query(Product).filter(Product.product_category=='1').all()
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
        else:
            total=0
        return render_template('user/shopmen.html',MFoot=men_footware,usercart=usercart,cartdeets=deetscart,total=total,year=date.today().year)
    else:
        return redirect('/customer/account/')
    

## Men Accesories Shopping Page
@app.route('/shop/men/accessories/')
def shop_men_accessories():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        todaysdate=date.today()
        men_accessories=db.session.query(Product).filter(Product.product_category=='2').all()
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
        else:
            total=0
        return render_template('user/male_accessories.html', menAcc=men_accessories, usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)
    else:
        return redirect('/customer/account/')
    
    
## Women Shopping Page
@app.route('/shop/women/')
def shop_women():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        todaysdate=date.today()
        women_footware=db.session.query(Product).filter(Product.product_category=='3').all()
        
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
        else:
            total=0
        return render_template('user/shopwomen.html', WFoot=women_footware, usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)
    else:
        return redirect('/customer/account/')



## Women Accessories Shopping Page
@app.route('/shop/women/accessories/')
def shop_women_accessores():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        todaysdate=date.today()
        women_accessories=db.session.query(Product).filter(Product.product_category=='4').all()
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
        else:
            total=0
        return render_template('user/female_accessories.html', women_acc=women_accessories, usercart=usercart,cartdeets=deetscart, total=total, year=date.today().year)
    else:
        return redirect('/customer/account/')


