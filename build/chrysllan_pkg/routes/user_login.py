from datetime import date
from flask import render_template,make_response,redirect,session,abort,request,flash,jsonify
from werkzeug.security import check_password_hash
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

    
## Login template
@app.route('/customer/login/')
def render_login_template():
    todaysdate = date.today()
    shopping_ID = session.get('user_cart_id')
    
    usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
    deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
        return render_template('user/loginpage.html', usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)
    else:
        total=0
        return render_template('user/loginpage.html', usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)


    
## User Login verification
@app.route('/user/login/', methods=['POST'])
def user_login_verification():
    user_email = request.form.get('login_email')
    user_password = request.form.get('login_pswd')
    
    if user_email!="" and user_password!="":
        user_deets=db.session.query(Customer).filter(Customer.cust_email==user_email).first()
        
        if user_deets and check_password_hash(user_deets.cust_pswd,user_password):
            session['username']=user_deets.cust_firstname
            session['user_id']=user_deets.cust_id
            return redirect("/chrisllan/")
        else:
            flash('Invalid Login Credentials', category='wrong_details')
            return redirect('/customer/login/')
    else:
        flash('Please fill out the form',category='wrong_details')
        return redirect('/customer/login/')


## User Logout Route
@app.route('/customer/logout/')
def user_logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user_cart_id', None)
    session.pop('txn_ref', None)
    return redirect('/')
