from datetime import date
from flask import render_template,make_response,redirect,session,abort,request,flash,jsonify
from chrysllan_pkg.routes.user_accounts import validate_email
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

@app.route('/subscribe_newsletter/', methods=['POST'])
def reg_newsletter():
    usermail=request.form.get('emailaddress')
    
    if usermail=="":
        return 'Please fill out all fields'
    else:
        email_validation = validate_email(usermail)
        
        if email_validation is True:
            check_email_presence = Newsletter_subscription.query.filter(Newsletter_subscription.email==usermail).first()
            if check_email_presence is None:
                add_to_newsletter = Newsletter_subscription(email = usermail, date_reg=date.today())
                db.session.add(add_to_newsletter)
                db.session.commit()
                return 'Successfully Registered'
            else:
                return 'Email Already Registered'
        else:
            return 'Please provide a valid email'