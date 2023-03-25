import random
from datetime import date
from flask import render_template, session, request, redirect
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

## Add to Cart
@app.route('/add/cart/')
def add_to_cart():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        productid = request.args.get('product')
        quantity = request.args.get('quantity')
        amount_payable = request.args.get('amount')
        user_cart_no = request.args.get('temp_id')
        today_date = date.today()
        
        is_product_in_cart = Cart.query.filter(Cart.user_cart_id==shopping_ID, Cart.product==productid).first()
        if is_product_in_cart:
            is_product_in_cart.product_qty = int(is_product_in_cart.product_qty) + int(quantity)
            is_product_in_cart.amount = int(is_product_in_cart.amount) + int(amount_payable)
            is_product_in_cart.cart_date = date.today()
            db.session.commit() 
            return "Item Added"
        else:
            add_to_cart=Cart(user_cart_id=user_cart_no, product=productid, product_qty=quantity, amount=amount_payable,cart_date=today_date)
            db.session.add(add_to_cart)
            db.session.commit()
            return "Item Added"
    else:
        return redirect('/')


   
## removecartitem
@app.route('/removeitem/')
def removeitem():
    item2remove=request.args.get('trash')
    
    discard_cart_item = db.session.query(Cart).get(item2remove)
    db.session.delete(discard_cart_item)
    db.session.commit()
    return "Item Deleted"



## empty cart
@app.route('/emptycart/')
def emptyCart():
    user_cart_id=request.args.get('emptycartID')
    incenerate_cart=db.session.query(Cart).filter(Cart.user_cart_id==user_cart_id).all()
    if incenerate_cart != []:
        for trash in incenerate_cart:
            db.session.delete(trash)
        db.session.commit()
        return "Cart Emptied"
    return "Cart Emptied"


def generate_transaction_reference():
    chars="1234567890"
    length_of_ref = [7,8,9]
    for id in range(1):
        identity=""
        for uniq in range(random.choice(length_of_ref)):
            identity = identity + random.choice(chars)
            
    return identity



def get_transaction_ref():
    get_txn_ref = generate_transaction_reference()
    
    found = True
    
    while found:
        result = Order.query.filter(Order.ref_no == get_txn_ref).first()
        if result:
            get_txn_ref = generate_transaction_reference()
        else:
            found = False
    return get_txn_ref



### confirm order in cart
@app.route('/confirm-order/', methods=['POST'])
def confirm_order():
    if session.get('user_id')!=None and session.get('username')!=None:
        if session.get('user_cart_id')!=None:
            
            total_amount = request.form.get('totalamt')
            cartID = request.form.get('userCartNumber')
            shipping = request.form.get('shipping_address')
            reference = get_transaction_ref()
            session['txn_ref'] = reference
            status = 'Pending'
            client = session.get("user_id")
            the_order_date = date.today()
            
            ## Register New Order
            new_order = Order(buyer=client, ref_no=reference, order_date=the_order_date, order_status=status, order_amount=total_amount, shipping_address=shipping, order_payment='Pending')
            db.session.add(new_order)
            db.session.commit()
            
            print(reference)
            # Register Order Details
            user_order_detail = Order.query.filter(Order.buyer==client, Order.ref_no==reference).first()
            print(user_order_detail)
            the_order_id = user_order_detail.order_id
            theamountPayable = user_order_detail.order_amount
            
            cartinfo = db.session.query(Cart).filter(Cart.user_cart_id==cartID).all()
            for i in cartinfo:
                register_order_detail = Order_details(order_id = the_order_id, prod_id=i.product, product_qty=i.product_qty, prod_price=i.amount)
                db.session.add(register_order_detail)
                #db.session.delete(i)
            db.session.commit()
            
            details_of_order = db.session.query(Order_details).filter(Order_details.order_id==the_order_id).all()
            
           
            #passing cart info to the route
            usercart=db.session.query(Cart).filter(Cart.user_cart_id==cartID).count()
            deetscart=db.session.query(Cart).filter(Cart.user_cart_id==cartID).all()
            if deetscart!=[]:
                total=0
                for i in deetscart:
                    total=total+i.amount
            else:
                total=0
                
            return render_template('user/informationpage.html', order_details=details_of_order, payable=theamountPayable,ref=reference, usercart=usercart, cartdeets=deetscart, total=total, year=date.today().year)
        else:
            return redirect('/')
    else:
        return redirect('/customer/login/')
