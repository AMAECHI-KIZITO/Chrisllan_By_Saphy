import re
from datetime import date
from flask import render_template,session, request
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from chrysllan_pkg import app, db, mail
from chrysllan_pkg.models import *

def validate_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return True
    else:
        return False
    
    
def send_welcome_mail(recipient, username):
    msg = Message("Welcome", sender=('Chrisllan By Saphy', 'konkakira1960@gmail.com'), recipients=[recipient])
    msg.html = render_template('welcome_to_chrisllan.html', recipient=recipient, username=username, year=date.today().year)
    mail.send(msg)
    return 200

   
## Create Account template
@app.route('/customer/account/')
def render_account_creation_template():
    todaysdate = date.today()
    shopping_ID = session.get('user_cart_id')
    
    usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
    deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
        return render_template('user/new_account.html',usercart=usercart,cartdeets=deetscart,total=total,year=date.today().year)
    else:
        total=0
        return render_template('user/new_account.html',usercart=usercart,cartdeets=deetscart,total=total,year=date.today().year)
   

  
## Create User Account
@app.route('/user_account_registration/',methods=['POST'])
def create_account():
    user_fname=request.form.get('firstname')
    user_lname=request.form.get('lastname')
    user_phone=request.form.get('phone')
    user_email=request.form.get('email')
    user_pswd=request.form.get('pswd')
    formatted_pswd=generate_password_hash(user_pswd)
    
    if user_fname!="" and user_lname!="" and user_phone!="" and user_email!="" and user_pswd!="":
        if len(user_phone)==11 and user_phone.isnumeric():
            valid_phone=re.findall("^(080)|^(081)|^(070)|^(090)", user_phone)
            if valid_phone:
                email_validation = validate_email(user_email)
                if email_validation is True:
                    try:
                        User=Customer(cust_firstname=user_fname,cust_lastname=user_lname,cust_phone=user_phone,cust_pswd=formatted_pswd,cust_email=user_email)
                        db.session.add(User)
                        db.session.commit()
                        welcome_user = send_welcome_mail(user_email, user_fname)
                        return f"Thank you. Registration Successful."
                    except:
                        return "Sorry. This email is already registered"
                else:
                    return "Sorry. Only gmail, yahoo and hotmail accounts are allowed"
            else:
                return "Invalid phone number format. Please provide a Nigerian number."
        else:
            return "Invalid Phone Number."
    else:
        return 'Please fill out all fields'
    
    
