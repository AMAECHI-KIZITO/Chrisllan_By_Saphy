import os,re,random,requests,json
from flask import render_template,make_response,redirect,session,abort,request,flash,request,jsonify
from sqlalchemy import func
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

## Home Page Route
@app.route('/')
@app.route('/chrisllan/')
def home():
    todaysdate=date.today()
    usercart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).count()
    deetscart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
    else:
        total=0        
    return render_template('user/index.html',usercart=usercart,cartdeets=deetscart,total=total)

## Create Account and Login Route
@app.route('/customer/account/')
def user_create_account():
    todaysdate=date.today()
    usercart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).count()
    deetscart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
    else:
        total=0
    return render_template('user/new_account.html',usercart=usercart,cartdeets=deetscart,total=total)

## Contact us Route
@app.route('/contact-us/')
def contactus():
    todaysdate=date.today()
    usercart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).count()
    deetscart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
    else:
        total=0
    return render_template('user/contactus.html',usercart=usercart,cartdeets=deetscart,total=total)


## Drop a contact message
@app.route('/drop_a_message/',methods=['POST'])
def leave_message():
    sender=request.form.get('name')
    sender_mail=request.form.get('email')
    sender_phone=request.form.get('phone')
    sender_msg=request.form.get('message')
    
    if sender=="" and sender_mail=="" and sender_phone=="" and sender_msg=="":
        return 'Please fill out all fields'
    elif sender_phone.isnumeric() and len(sender_phone)==11 and '@' in sender_mail and sender_mail.endswith('.com') and sender_phone.startswith('080') or sender_phone.startswith('070') or sender_phone.startswith('090') or sender_phone.startswith('081'):
        C=Contact_us(name=sender, email=sender_mail, phone=sender_phone, message=sender_msg)
        db.session.add(C)
        db.session.commit()
        return "Thank You. Message sent."
    else:
        return "Error. Ensure that a valid phone number and email was provided then try again"
        

## Shopping Page
@app.route('/shop/')
def shop():
    todaysdate=date.today()
    usercart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).count()
    men_footware=db.session.query(Product).filter(Product.product_category=='1').all()
    women_footware=db.session.query(Product).filter(Product.product_category=='3').all()
    men_accessories=db.session.query(Product).filter(Product.product_category=='2').all()
    deetscart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).all()
    
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
    else:
        total=0
    return render_template('user/shop.html',MFoot=men_footware,WFoot=women_footware,menAcc=men_accessories,usercart=usercart,cartdeets=deetscart,total=total)

## Men Footware Shopping Page
@app.route('/shop/men/')
def shop_men():
    todaysdate=date.today()
    usercart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).count()
    men_footware=db.session.query(Product).filter(Product.product_category=='1').all()
    deetscart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
    else:
        total=0
    return render_template('user/shopmen.html',MFoot=men_footware,usercart=usercart,cartdeets=deetscart,total=total)

## Men Accesories Shopping Page
@app.route('/shop/men/accessories/')
def shop_men_accessories():
    todaysdate=date.today()
    usercart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).count()
    men_accessories=db.session.query(Product).filter(Product.product_category=='2').all()
    deetscart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
    else:
        total=0
    return render_template('user/male_accessories.html',menAcc=men_accessories,usercart=usercart,cartdeets=deetscart,total=total)

## Women Shopping Page
@app.route('/shop/women/')
def shop_women():
    todaysdate=date.today()
    usercart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).count()
    women_footware=db.session.query(Product).filter(Product.product_category=='3').all()
    deetscart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
    else:
        total=0
    return render_template('user/shopwomen.html',WFoot=women_footware,usercart=usercart,cartdeets=deetscart,total=total)


## Women Accessories Shopping Page
@app.route('/shop/women/accessories/')
def shop_women_accessores():
    todaysdate=date.today()
    usercart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).count()
    women_accessories=db.session.query(Product).filter(Product.product_category=='4').all()
    deetscart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
    else:
        total=0
    return render_template('user/female_accessories.html',women_acc=women_accessories,usercart=usercart,cartdeets=deetscart,total=total)


## Subscribe Newsletter
@app.route('/subscribe_newsletter/',methods=['POST'])
def reg_newsletter():
    usermail=request.form.get('emailaddress')
    the_csrf=request.form.get('csrf_token')
    
    if usermail=="":
        return 'Please fill out all fields'
    else:
        if usermail.endswith('@gmail.com'):
            with open('newsletter.txt','a')as file:
                file.write(f"{usermail} \n")
            return 'Successfully Registered'
        else:
            return 'Please provide a valid Google mail account'
        

## Create Account User
@app.route('/user_account_registration/',methods=['POST'])
def create_account():
    user_fname=request.form.get('firstname')
    user_lname=request.form.get('lastname')
    user_phone=request.form.get('phone')
    user_email=request.form.get('email')
    user_pswd=request.form.get('pswd')
    formatted_pswd=generate_password_hash(user_pswd)
    
    if user_fname!="" and user_lname!="" and user_phone!="" and user_email!="" and user_pswd!="":
        if len(user_phone)==11 and user_phone.isnumeric():
            valid_phone=re.findall("^(080)|^(081)|^(070)|^(090)",user_phone)
            if valid_phone:
                if user_email.endswith('@gmail.com') or user_email.endswith('@yahoo.com') or user_email.endswith('@hotmail.com'):
                    try:
                        User=Customer(cust_firstname=user_fname,cust_lastname=user_lname,cust_phone=user_phone,cust_pswd=formatted_pswd,cust_email=user_email)
                        db.session.add(User)
                        db.session.commit()
                        return f"Thank you. Registration Successful."
                    except:
                        return "Sorry. This email is already registered"
                else:
                    return "Sorry. Only gmail, yahoo and hotmail accounts are allowed"
            else:
                return "Invalid phone number format. Please provide a Nigerian number."
        else:
            return "Invalid Phone Number."
    
    else:
        return 'Please fill out all fields'
    
    
## User Login
@app.route('/user/login/',methods=['POST'])
def user_login():
    user_email=request.form.get('login_email')
    user_code=request.form.get('login_pswd')
    
    if user_email!="" and user_code!="":
        user_deets=db.session.query(Customer).filter(Customer.cust_email==user_email).first()
        
        if user_deets:
            allowed_email=user_deets.cust_email
            protected=user_deets.cust_pswd
            if user_email==allowed_email and check_password_hash(protected,user_code):
                session['username']=user_deets.cust_firstname
                session['user_id']=user_deets.cust_id
                return redirect("/chrisllan/")
            else:
                flash('Details Incorrect',category='wrong_details')
                return redirect('/customer/account/')
            
        else:
            flash('Invalid Login Credentials',category='wrong_details')
            return redirect('/customer/account/')
    else:
        flash('Please fill out the form',category='wrong_details')
        return redirect('/customer/account/')
    
## User Logout Route
@app.route('/customer/logout/')
def user_logout():
    session.pop('user_id',None)
    session.pop('username',None)
    return redirect('/')

## Subscribe Newsletter
@app.route('/add/cart/<id>',methods=['POST'])
def test(id):
    if session.get('user_id')!=None and session.get('username')!=None:
        prod_deets=db.session.query(Product).get(id)
        itemID=prod_deets.product_id
        itemPrice=prod_deets.product_price
        client=session.get('user_id')
        quantity='1'
        thedate=date.today()
        NewCart=Cart(buyer_id=client,product=itemID,product_qty=quantity,amount=itemPrice,cart_date=thedate)
        
        db.session.add(NewCart)
        db.session.commit()
        flash('Item added to cart',category='itemAdded')
        return redirect('/shop/')
        
    else:
        flash('Dear Customer, kindly register or login to proceed.', category='reg_needed')
        return redirect('/customer/account')
    
## removecartitem
@app.route('/removeitem/<id>')
def removeitem(id):
    itemtoremove=db.session.query(Cart).get(id)
    db.session.delete(itemtoremove)
    db.session.commit()
    flash('Item Removed',category='itemOut')
    return redirect ('/shop/')

## empty cart
@app.route('/emptycart/')
def emptyCart():
    thedate=date.today()
    itemtoremove=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'),Cart.cart_date==thedate).all()
    for i in itemtoremove:
        db.session.delete(i)
        db.session.commit()
    flash('Cart Empty',category='itemOut')
    return redirect ('/shop/')

### Update cart quantity
@app.route('/confirm_order/',methods=['POST'])
def confirmOrder():
    total_amount=request.form.get('totalamt')
    shipping=request.form.get('shipping_address')
    reference=int((random.random() * 1000000000)+1)
    session['txn_ref']=reference
    status='Pending'
    client=session.get("user_id")
    the_order_date=date.today()
    
    ## This adds to the order table
    Ord=Order(buyer=client,ref_no=reference,order_date=the_order_date,order_status=status,order_amount=total_amount, shipping_address=shipping)
    db.session.add(Ord)
    db.session.commit()
    
    #to add to order details table
    userOrderId=db.session.query(Order).filter(Order.buyer==session.get('user_id'),Order.ref_no==reference).first()
    OrddID=userOrderId.order_id
    cart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'),Cart.cart_date==the_order_date).all()
    for i in cart:
        Ord_DET=Order_details(order_id=OrddID,prod_id=i.product,prod_price=i.amount)
        db.session.add(Ord_DET)
        db.session.delete(i)
    db.session.commit()
    
    ## This is to show the customer the info and initialize payment
    orderinfo=db.session.query(Order).filter(Order.ref_no==reference, Order.buyer==session.get('user_id')).first()
    theOrderID=orderinfo.order_id
    theamountPayable=orderinfo.order_amount
    orderdeetsinfo=db.session.query(Order_details).filter(Order_details.order_id==theOrderID).all()
    
    ## Adding to payment table
    Txn=Payment(pay_orderid=theOrderID, pay_amt=theamountPayable,pay_ref=reference,pay_status="Pending")
    db.session.add(Txn)
    db.session.commit()
    
    #passing cart info to the route
    todaysdate=date.today()
    usercart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).count()
    deetscart=db.session.query(Cart).filter(Cart.buyer_id==session.get('user_id'), Cart.cart_date==todaysdate).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
    else:
        total=0
    return render_template('user/informationpage.html',Ord_Details=orderdeetsinfo, payable=theamountPayable,ref=reference,usercart=usercart,cartdeets=deetscart,total=total)

# Order Info Page
@app.route('/call/paystack/')
def paystack():
    if session.get('user_id')!=None and session.get('username')!=None:
        loggedin=session.get('user_id')
        orderinfo=db.session.query(Order).filter(Order.ref_no==session.get('txn_ref')).first()
        buyerinfo=db.session.query(Customer).get(loggedin)
        
        #here we send info to paystack
        data = {"email":buyerinfo.cust_email,"amount":orderinfo.order_amount*100, "reference":session.get('txn_ref')}
        headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_2d885e99a5f8c0ca434f5862d78a5de5603962cd"}
        response = requests.post("https://api.paystack.co/transaction/initialize",headers=headers, data=json.dumps(data))
        rsp_json = response.json()
        
        #return rsp_json....It will result in a message like shown below
        # {
        #     "data": {
        #         "access_code": "3upv551a9azib4e", 
        #         "authorization_url": "https://checkout.paystack.com/3upv551a9azib4e", 
        #         "reference": "688931979"
        #     }, 
        #     "message": "Authorization URL created", 
        #     "status": true
        # }
        
        if rsp_json['status'] == True:
            url = rsp_json['data']['authorization_url']
            return redirect(url)
        else:
            flash("Unable to complete. Please try again",category='payerror')
            return redirect('/shop/')
    else:
        return redirect('/customer/account/')
    
## Second API consumption phase
@app.route('/paystack_landing/')
def paystack_landing():
    """This route would have been configured in the paystack developer dashboard, this is where user would be redirected to after inputing their card details, here you will confirm the transaction status and update your db accordingly"""

    if session.get('user_id')!=None and session.get('username')!=None:
        loggedin = session.get('user_id')
        ref = session.get('txn_ref')
        pay_ord_id = Payment.query.filter(Payment.pay_ref==ref).first()
        pOID=pay_ord_id.pay_orderid
        headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_2d885e99a5f8c0ca434f5862d78a5de5603962cd"}
        response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
        rsp_json = response.json() 
        #uncomment this out to see the structure of what paystack returns, then you would be able to pick what you need
        #return rsp_json... This will give something like this
        
        # {
        #     "status": true,
        #     "message": "Verification successful",
        #     "data": {
        #         "amount": 27000,
        #         "currency": "NGN",
        #         "transaction_date": "2016-10-01T11:03:09.000Z",
        #         "status": "success",
        #         "reference": "DG4uishudoq90LD",
        #         "domain": "test",
        #         "metadata": 0,
        #         "gateway_response": "Successful",
        #         "message": null,
        #         "channel": "card",
        #         "ip_address": "41.1.25.1",
        #         "log": {
        #         "time_spent": 9,
        #         "attempts": 1,
        #         "authentication": null,
        #         "errors": 0,
        #         "success": true,
        #         "mobile": false,
        #         "input": [],
        #         "channel": null,
        #         "history": [{
        #             "type": "input",
        #             "message": "Filled these fields: card number, card expiry, card cvv",
        #             "time": 7
        #             },
        #             {
        #             "type": "action",
        #             "message": "Attempted to pay",
        #             "time": 7
        #             },
        #             {
        #             "type": "success",
        #             "message": "Successfully paid",
        #             "time": 8
        #             },
        #             {
        #             "type": "close",
        #             "message": "Page closed",
        #             "time": 9
        #             }
        #         ]
        #         }
        #         "fees": null,
        #         "authorization": {
        #         "authorization_code": "AUTH_8dfhjjdt",
        #         "card_type": "visa",
        #         "last4": "1381",
        #         "exp_month": "08",
        #         "exp_year": "2018",
        #         "bin": "412345",
        #         "bank": "TEST BANK",
        #         "channel": "card",
        #         "signature": "SIG_idyuhgd87dUYSHO92D",
        #         "reusable": true,
        #         "country_code": "NG",
        #         "account_name": "BoJack Horseman"
        #         },
        #         "customer": {
        #         "id": 84312,
        #         "customer_code": "CUS_hdhye17yj8qd2tx",
        #         "first_name": "BoJack",
        #         "last_name": "Horseman",
        #         "email": "bojack@horseman.com"
        #         },
        #         "plan": "PLN_0as2m9n02cl0kp6",
        #         "requested_amount": 1500000
        #     }
        # }
        
        if rsp_json['status'] == True: 
            data = rsp_json['data']
            actual_amt = data['amount']/100
            feedback = data['gateway_response']
            #update payment table
            pay = Payment.query.filter(Payment.pay_ref==ref).first()
            pay.pay_status = 'Paid'
            pay.pay_feedback =feedback
            db.session.commit()
            
            flash("Successfully Paid. Thank you for your patronage",  category='payment_successful')
            return redirect('/shop/') 
            # or direct the user to their dashboard where they would see their transaction history as Paid
        else:
            data = rsp_json['data']
            actual_amt = data['amount']/100
            feedback = data['gateway_response']
            pay = Payment(pay_orderid=pOID,pay_amt=actual_amt,pay_status='Failed',pay_feedback='Transaction Failed')
            db.session.add(pay)
            db.session.commit()
            flash("Payment Unsuccessful. Please try again.",  category='payment_unsuccessful')
            return redirect('/shop/') 
    else:
        return redirect('/customer/account/')


        
# ### WEBHOOK URL        
# @app.route('/paystack_webhook/',methods=['POST'])
# def paystack_webhook():
    

#     if session.get('user_id')!=None and session.get('username')!=None:
#         return 'hello'
#     else:
#         return redirect('/customer/account/')

### ERROR 404 and 500 Pages
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('user/chrisllan500error.html',error=error),500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('user/chrisllan404error.html',error=error),404