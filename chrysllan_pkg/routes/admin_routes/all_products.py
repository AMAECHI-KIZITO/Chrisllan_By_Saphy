import os
from datetime import date
from flask import render_template, redirect, session, request, flash
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

## All Products Template
@app.route('/admin/allproducts/')
def all_products():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        products=db.session.query(Product).all()
        return render_template('admin/allproducts.html', products=products)
    else:
        return redirect('/admin/')