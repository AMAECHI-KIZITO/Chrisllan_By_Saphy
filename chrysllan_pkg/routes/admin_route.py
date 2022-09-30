import os
from flask import render_template,make_response,redirect,session,abort,request,flash,jsonify
from sqlalchemy import func
from datetime import date
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

@app.route('/chrisllan/admin/login/')
def admin_login():
    return render_template('admin/admin_login.html')


## ADMIN VERIFY LOGIN       
@app.route('/admin/login/',methods=['POST'])
def admin_verify_login():
    admin_email=request.form.get('admin_email')
    admin_pswd=request.form.get('admin_pswd')
    checkdeets=db.session.query(Admin).filter(Admin.admin_email==admin_email, Admin.admin_pswd==admin_pswd).first()
    if checkdeets:
        session['admin_name']=checkdeets.admin_firstname
        session['admin_id']=checkdeets.admin_id
        day=date.today()
        totalcust=db.session.query(Customer).count()
        totalorders=db.session.query(Order).count()
        todayorder=db.session.query(Order).filter(Order.order_date==day).count()
        return render_template('admin/admindashboard.html',cust=totalcust, allorder=totalorders, todayorder=todayorder)
    else:
        flash('Incorrect Credentials', category='wrong_admin_login')
        return redirect('/chrisllan/admin/login/')
    
      
## Admin Home Dashboard
@app.route('/admin/dashboard/')
def admin_Home():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        day=date.today()
        totalcust=db.session.query(Customer).count()
        totalorders=db.session.query(Order).count()
        todayorder=db.session.query(Order).filter(Order.order_date==day).count()
        return render_template('admin/admindashboard.html',cust=totalcust, allorder=totalorders, todayorder=todayorder)
    else:
        return redirect('/chrisllan/admin/login/')
    



    
@app.after_request
def clearcache(response):
    response.headers['Cache-Control']="no-cache, no store, must-revalidate"
    return response


@app.route('/admin/logout/')
def admin_logout():
    session.pop('admin_name',None)
    session.pop('admin_id',None)
    return redirect('/chrisllan/admin/login/')


## Add Product Template
@app.route('/admin/add/product/')
def addproducts():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        categories=db.session.query(Category).all()
        return render_template('admin/admin_addproduct.html',category=categories)
    else:
        return redirect('/chrisllan/admin/login/')
    
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
            original_filename=prod_img.filename
            name,extension=os.path.splitext(original_filename)
            
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
        return redirect('/chrisllan/admin/login/')
    
    
## All Products Template
@app.route('/admin/allproducts/')
def all_products():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        products=db.session.query(Product).all()
        return render_template('admin/allproducts.html',products=products)
    else:
        return redirect('/chrisllan/admin/login/')
    
## All Orders
@app.route('/admin/allorders/')
def all_orders():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        allorders=db.session.query(Order).order_by(Order.order_date.desc()).all()
        return render_template('admin/allorders.html',allorders=allorders)
    else:
        return redirect('/chrisllan/admin/login/')
    
## All Messages from contact us
@app.route('/admin/messages/')
def all_messages():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        messages=db.session.query(Contact_us).all()
        return render_template('admin/allmessages.html',msg=messages)
    else:
        return redirect('/chrisllan/admin/login/')
    
## View Orders
@app.route('/vieworder/<id>')
def view_order_details(id):
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        specific=db.session.query(Order_details).filter(Order_details.order_id==id).all()
        paystatus=db.session.query(Payment).filter(Payment.pay_orderid==id).first()
        price=db.session.query(Order).filter(Order.order_id==id).first()
        amt=price.order_amount
        return render_template('admin/vieworder.html',specific=specific,id=id,amt=amt,paystatus=paystatus)
    else:
        return redirect('/chrisllan/admin/login/')
    
## Update Order Status
@app.route('/update_order_status/<id>', methods=['POST'])
def update_order_status(id):
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        specific=db.session.query(Order).filter(Order.order_id==id).first()
        specific.order_status='Completed'
        db.session.commit()
        return redirect('/admin/allorders/')
    else:
        return redirect('/chrisllan/admin/login/')
    
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
        return redirect('/chrisllan/admin/login/')



## Edit Product Search Template
@app.route('/admin/edit/product/')
def edit_product():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        return render_template('admin/edit_product.html')
    else:
        return redirect('/chrisllan/admin/login/')
    
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
        return redirect('/chrisllan/admin/login/')

## Update Item Template
@app.route('/update/product/<id>')
def update_item(id):
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        item_to_update=db.session.query(Product).filter(Product.product_id==id).all()
        return render_template('admin/update_product.html', update=item_to_update)
    else:
        return redirect('/chrisllan/admin/login/')
    
    
## The Actual Update
@app.route('/product_update/',methods=['POST'])
def updatedproducts():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        allowed=['.jpeg','.jpg']
        prod_name=request.form.get('product_name')
        prod_category=request.form.get('prod_cat')
        prod_price=request.form.get('product_price')
        prod_img=request.files.get('product_image')
        id=request.form.get('prod_id')
        
        if prod_name!="" and prod_category!="" and prod_category!='#' and prod_price!="" and prod_img!="" and id!="":
            original_filename=prod_img.filename
            name,extension=os.path.splitext(original_filename)
            
            if extension in allowed:
                originalfile = "chrysllan_pkg/static/productimages/"+original_filename
                prod_img.save(originalfile)
                
                PROD_UPDATE=db.session.query(Product).get(id)
                PROD_UPDATE.product_name=prod_name
                PROD_UPDATE.product_price=prod_price
                PROD_UPDATE.product_image=original_filename
                db.session.commit()
                return f'Successfully updated product'
            else:
                return "Please upload a .jpg or .jpeg image." 
        else:
            return "Please ensure fields are filled and a valid category is selected"
    else:
        return redirect('/chrisllan/admin/login/')


## View Message
@app.route('/view/message/<id>')
def view_message_details(id):
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        specific=db.session.query(Contact_us).filter(Contact_us.contact_us_id==id).first()
        return render_template('admin/viewmessage.html',specific=specific)
    else:
        return redirect('/chrisllan/admin/login/')
    
## Admin Password Change Template
@app.route('/admin/passwordchange/')
def admin_password_change():
    if session.get("admin_id")!=None and session.get("admin_name")!=None:
        return render_template("admin/admin_changepassword.html")
    else:
        return redirect('/chrisllan/admin/login/')
    
## Admin Password Change Form
@app.route('/admin/pswd_change/',methods=['POST'])
def admin_pswd_change():
    if session.get("admin_id")!=None and session.get("admin_name")!=None:
        # This is to retrieve current admin info
        admin=session.get("admin_id")
        admindeets=db.session.query(Admin).get(admin)
        
        # This is to get the form data
        form_old_pswd=request.form.get("old_pswd")
        form_new_pswd=request.form.get("new_pswd")
        form_confirm_pswd=request.form.get("new_pswd_confirm")
        
        if admindeets:
            currentpswd=admindeets.admin_pswd
            if form_old_pswd!="" and form_new_pswd!="" and form_confirm_pswd!="":
                if currentpswd==form_old_pswd and form_new_pswd==form_confirm_pswd:
                    admindeets.admin_pswd=form_confirm_pswd
                    db.session.commit()
                    return "Password Successfully Changed"
                else:
                    return "Password Not Changed. Ensure details are correct"
            else:
                return "Please complete all fields"
        else:
            return redirect('/chrisllan/admin/login/')
            
    else:
        return redirect('/chrisllan/admin/login/')