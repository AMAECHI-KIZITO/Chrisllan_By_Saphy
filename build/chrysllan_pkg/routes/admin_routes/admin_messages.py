from datetime import date
from flask import render_template, redirect, session, request, flash
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *


## All Messages from contact us
@app.route('/admin/messages/')
def all_messages():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        messages=db.session.query(Contact_us).all()
        return render_template('admin/allmessages.html', msg=messages)
    else:
        return redirect('/admin/')
    

## View Message
@app.route('/view/message/<id>')
def view_message_details(id):
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        specific=db.session.query(Contact_us).filter(Contact_us.contact_us_id==id).first()
        return render_template('admin/viewmessage.html', specific=specific)
    else:
        return redirect('/admin/')