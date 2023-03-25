import requests, json
from datetime import date
from flask import render_template, session, redirect, request, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from werkzeug.security import generate_password_hash
from chrysllan_pkg import app,db, mail
from chrysllan_pkg.config import LiveConfig
from chrysllan_pkg.models import *

serializer=URLSafeTimedSerializer(LiveConfig.FORGOT_PSWD_KEY)


def send_reset_password_mail(recipient, reset_link, username):
    msg = Message("Reset Your Password", sender=('Chrisllan By Saphy', 'konkakira1960@gmail.com'), recipients=[recipient])
    msg.html = render_template('forgot_password_mail.html', reset_link=reset_link, recipient=recipient, username=username, year=date.today().year)
    mail.send(msg)
    return 200

@app.route("/user-forgot-password/", methods=['POST'])
def send_reset_link():
    user_email = request.form.get("forgotPasswordEmailAddress")
    
    if user_email:
        user_record = Customer.query.filter(Customer.cust_email==user_email).first()
        
        if user_record:
            customer_name = user_record.cust_firstname
            token = serializer.dumps(user_email, salt='forgot-password-confirm')
            reset_link = url_for('validate_reset_forgot_password_link', token=token, _external=True)
            
            send_mail = send_reset_password_mail(user_email, reset_link, customer_name)
            return f"A reset password link has been sent to {user_email}"
        else:
            return f"A reset password link has been sent to {user_email}"
        
        
        
# forgot password mail link validation
@app.route('/reset-forgot-password/<token>')
def validate_reset_forgot_password_link(token):
    try:
        user_email = serializer.loads(token, salt='forgot-password-confirm', max_age=900)
        checking_email = Customer.query.filter(Customer.cust_email==user_email).first()
        
        if checking_email:
            return render_template('user/reset_forgot_password.html', status="reset-password", email=user_email)
    except SignatureExpired:
        return render_template('user/reset_forgot_password.html', status="token-expired")
    except BadTimeSignature:
        return render_template('user/reset_forgot_password.html', status="invalid-token")
    
# # forgot password mail link validation
# @app.route('/formpage/')
# def ddd():
#     return render_template('user/reset_forgot_password.html', status="reset-password", email="kkk@k.vom")


# change password submission
@app.route('/reset-account-password/', methods=['POST'])
def submit_reset_password():
    user_email = request.form.get('userEmail')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')
    
    if user_email and new_password and confirm_password:
        user_record = Customer.query.filter(Customer.cust_email==user_email).first()
        if ' ' in new_password or ' ' in confirm_password:
            return "Reset failed! Passwords cannot contain whitespace"
        else:
            if user_record and new_password == confirm_password:
                encrypted_password = generate_password_hash(new_password)
                user_record.cust_pswd = encrypted_password
                db.session.commit()
                return "Password Reset Successful"
            else:
                return "Reset failed! Ensure passwords match"
    else:
        return "Incomplete form data"