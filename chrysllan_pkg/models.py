from datetime import datetime,date
from chrysllan_pkg import db


class Admin(db.Model):
    admin_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    admin_firstname=db.Column(db.String(30), nullable=False)
    admin_lastname=db.Column(db.String(30), nullable=False)
    admin_email=db.Column(db.String(80), nullable=False)
    admin_pswd=db.Column(db.String(200),nullable=False)
 

    
class Customer(db.Model):
    cust_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cust_firstname=db.Column(db.String(30), nullable=False)
    cust_lastname=db.Column(db.String(30), nullable=False)
    cust_phone=db.Column(db.String(15), nullable=False)
    cust_regdate=db.Column(db.Date(), nullable=False, default=datetime.now())
    cust_email=db.Column(db.String(80), nullable=False, unique=True)
    cust_pswd=db.Column(db.String(200),nullable=False)
    
class Category(db.Model):
    cat_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cat_name=db.Column(db.String(50), nullable=False)
  
    
class Product(db.Model):
    product_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    product_name=db.Column(db.String(50), nullable=False)
    product_category=db.Column(db.Integer(), db.ForeignKey('category.cat_id')) #FK
    product_price=db.Column(db.Float(), nullable=False)
    product_image=db.Column(db.String(50), nullable=False)
    
    prods_cat_family=db.relationship('Category',backref='prod_deets')
 
    
class Cart(db.Model):
    cart_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_cart_id=db.Column(db.Integer(), nullable=False)
    product=db.Column(db.Integer(), db.ForeignKey('product.product_id')) #FK
    product_qty=db.Column(db.Integer(), nullable=False)
    amount=db.Column(db.Float(), nullable=False)
    cart_date=db.Column(db.Date(), nullable=False)
    
    cartprods=db.relationship('Product',backref='usercart_deets')


class Order(db.Model):
    order_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    buyer=db.Column(db.Integer(), db.ForeignKey('customer.cust_id'))#FK
    shipping_address=db.Column(db.Text(),nullable=False)
    ref_no=db.Column(db.Integer(), nullable=False)
    order_date=db.Column(db.Date(), nullable=False, default=date.today())
    order_status=db.Column(db.Enum('Completed', 'Pending','Network Failed'), nullable=False)
    order_amount=db.Column(db.Float(), nullable=False)
    order_payment=db.Column(db.Enum('Paid', 'Pending', 'Failed'), nullable=True, default='Pending')
    
    
    who_ordered=db.relationship('Customer',backref='cust_orders')

    
class Order_details(db.Model):
    details_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    order_id=db.Column(db.Integer(), db.ForeignKey('order.order_id'))#FK
    prod_id=db.Column(db.Integer(), db.ForeignKey('product.product_id'))#FK
    product_qty=db.Column(db.Integer(), nullable=False)
    prod_price=db.Column(db.Float(), nullable=False)
    
    Ord_details_prod_info=db.relationship('Product',backref='orderdetails_deets')
    
  
    
class Payment(db.Model):
    pay_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    pay_orderid =db.Column(db.Integer(), db.ForeignKey('order.order_id'))
    pay_amt=db.Column(db.Float(), nullable=False)
    pay_ref=db.Column(db.Integer(), nullable=False, unique=True)
    pay_date=db.Column(db.DateTime(), default=datetime.now())
    pay_status=db.Column(db.Enum('Paid', 'Pending', 'Failed'), nullable=True, default='Pending')
    pay_feedback=db.Column(db.String(255), nullable=True)
  
    
class Contact_us(db.Model):
    contact_us_id=db.Column(db.Integer(),primary_key=True, autoincrement=True, nullable=False)
    name=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    phone=db.Column(db.String(11),nullable=False)
    message=db.Column(db.Text(),nullable=False)
    date_sent=db.Column(db.DateTime(),default=date.today())
    
class Newsletter_subscription(db.Model):
    id=db.Column(db.Integer(),primary_key=True, autoincrement=True, nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    date_reg=db.Column(db.Date(),default=date.today())