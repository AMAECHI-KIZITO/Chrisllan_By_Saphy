import os
from datetime import date
from flask import render_template, redirect, session, request, flash
from werkzeug.utils import secure_filename
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

## Edit Product Search Template
@app.route('/admin/edit/product/')
def edit_product():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        return render_template('admin/edit_product.html')
    else:
        return redirect('/admin/')
    
    
@app.route('/edit/item/',methods=['POST'])
def edit_item():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        item_name=request.form.get('item')
        look=db.session.query(Product).filter(Product.product_name.ilike(f"%{item_name}%")).all()
        if item_name!="":
            if look:
                return render_template('admin/itemfound.html', look=look)
            else:
                flash('No Product Match Your Search', category='item_not_found')
                return render_template('admin/edit_product.html')  
        else:
            flash('Fields cannot be empty', category='item_not_found')
            return render_template('admin/edit_product.html') 
    else:
        return redirect('/admin/')



## Update Item Template
@app.route('/update/product/<id>')
def update_item(id):
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        item_to_update=db.session.query(Product).filter(Product.product_id==id).all()
        return render_template('admin/update_product.html', update=item_to_update)
    else:
        return redirect('/admin/')
    
    
## The Actual Update
@app.route('/product_update/',methods=['POST'])
def updatedproducts():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        allowed=['.jpeg','.jpg']
        prod_name = request.form.get('product_name')
        prod_category = request.form.get('prod_cat')
        prod_price = request.form.get('product_price')
        prod_img = request.files.get('product_image')
        id = request.form.get('prod_id')
        
        if prod_name!="" and prod_category!="" and prod_category!='#' and prod_price!="" and prod_img!="" and id!="":
            original_filename = secure_filename(prod_img.filename)
            name,extension = os.path.splitext(original_filename)
            
            if extension in allowed:
                originalfile = "chrysllan_pkg/static/productimages/"+original_filename
                prod_img.save(originalfile)
                
                prod_update=db.session.query(Product).get(id)
                prod_update.product_name=prod_name
                prod_update.product_price=prod_price
                prod_update.product_image=original_filename
                db.session.commit()
                
                return f'Successfully updated product'
            else:
                return "Please upload a .jpg or .jpeg image." 
        else:
            return "Please ensure fields are filled and a valid category is selected"
    else:
        return redirect('/admin/')
    

## Delete Product 
@app.route('/delete/product/<id>')
def delete_product(id):
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        discard=db.session.query(Product).get(id)
        db.session.delete(discard)
        db.session.commit()
        flash(f'Successfully deleted {discard.product_name}', category='discarded')
        return redirect('/admin/allproducts/')
    else:
        return redirect('/admin/')