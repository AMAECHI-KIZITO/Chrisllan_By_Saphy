import os
from datetime import date
from flask import render_template, redirect, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

## Admin Password Change Template
@app.route('/admin/passwordchange/')
def admin_password_change():
    if session.get("admin_id")!=None and session.get("admin_name")!=None:
        return render_template("admin/admin_changepassword.html")
    else:
        return redirect('/admin/')
    
## Admin Password Change Form
@app.route('/admin/pswd-change/',methods=['POST'])
def admin_pswd_change():
    if session.get("admin_id")!=None and session.get("admin_name")!=None:
        
        form_old_pswd=request.form.get("old_pswd")
        form_new_pswd=request.form.get("new_pswd")
        form_confirm_pswd=request.form.get("new_pswd_confirm")
        
        if form_old_pswd!="" and form_new_pswd!="" and form_confirm_pswd!="":
            admindeets=db.session.query(Admin).get(session.get("admin_id"))
            currentpswd = admindeets.admin_pswd
            
            if form_new_pswd == form_confirm_pswd and check_password_hash(currentpswd, form_old_pswd):
                admindeets.admin_pswd = generate_password_hash(form_confirm_pswd)
                db.session.commit()
                return "Password Successfully Changed"
            else:
                return "Password Not Changed. Ensure details are correct"
        else:
            return "Please complete all fields"
            
    else:
        return redirect('/admin/')