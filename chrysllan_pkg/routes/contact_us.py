from datetime import date
from flask import render_template, session, request
from chrysllan_pkg.routes.user_accounts import validate_email
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

    

## Contact us template
@app.route('/contact-us/')
def render_contact_us_template():
    todaysdate=date.today()
    shopping_ID = session.get('user_cart_id')
    
    usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
    deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
        return render_template('user/contactus.html', usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)
    else:
        total=0
        return render_template('user/contactus.html', usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)


## Drop a contact message
@app.route('/drop_a_message/',methods=['POST'])
def leave_message():
    sender=request.form.get('name')
    sender_mail=request.form.get('email')
    sender_phone=request.form.get('phone')
    sender_msg=request.form.get('message')
    
    
    if sender == "" and sender_mail == "" and sender_phone == "" and sender_msg == "":
        return 'Please fill out all fields'
    else:
        valid_mail = validate_email(sender_mail)
        
        if valid_mail is True and sender_phone.isnumeric() and len(sender_phone)==11 and sender_phone.startswith('080') or sender_phone.startswith('070') or sender_phone.startswith('090') or sender_phone.startswith('081'):
            new_message = Contact_us(name=sender, email=sender_mail, phone=sender_phone, message=sender_msg)
            db.session.add(new_message)
            db.session.commit()
            return "Thank You. Message sent."
        else:
            return "Error. Ensure that a valid phone number and email was provided then try again"
        