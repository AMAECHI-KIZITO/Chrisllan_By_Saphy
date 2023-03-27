import os
from datetime import date
from flask import render_template, redirect, session, request, flash
from werkzeug.utils import secure_filename
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

## Add Product Template
@app.route('/admin/add/product/')
def addproducts():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        categories=db.session.query(Category).all()
        return render_template('admin/admin_addproduct.html',category=categories)
    else:
        return redirect('/admin/')

    
## This is the form for product addition
@app.route('/product_addition/',methods=['POST'])
def newproducts():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        allowed=['.jpeg','.jpg']
        
        prod_name=request.form.get('product_name')
        prod_category=request.form.get('product_category')
        prod_price=request.form.get('product_price')
        prod_img=request.files.get('product_image')
        
        if prod_name!="" and prod_category!="" and prod_category!='#' and prod_price!="" and prod_img!="":
            original_filename = secure_filename(prod_img.filename)
            name,extension = os.path.splitext(original_filename)
            
            if extension in allowed:
                originalfile = "chrysllan_pkg/static/productimages/"+original_filename
                prod_img.save(originalfile)
                
                PROD=Product(product_name=prod_name,product_category=prod_category,product_price=prod_price,product_image=original_filename)
                db.session.add(PROD)
                db.session.commit()
                return f'Successfully added product'
            else:
                return "Please upload a .jpg or .jpeg image." 
        else:
            return "Please ensure fields are filled and a valid category is selected"
    else:
        return redirect('/admin/')