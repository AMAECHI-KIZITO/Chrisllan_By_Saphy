import os,re,random,requests,json
from flask import render_template,make_response,redirect,session,abort,request,flash,jsonify
from sqlalchemy import func
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

## Home Page Route
@app.route('/')
@app.route('/chrisllan/')
def home():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID == None:
        session['user_cart_id']=int(random.random()*452358)
        shopping_ID = session.get('user_cart_id')
        
        todaysdate=date.today()
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
            return render_template('user/index.html',usercart=usercart,cartdeets=deetscart,total=total)
        else:
            total=0        
            return render_template('user/index.html',usercart=usercart,cartdeets=deetscart,total=total)
    else:
        shopping_ID = session.get('user_cart_id')
        todaysdate=date.today()
        
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
            return render_template('user/index.html',usercart=usercart,cartdeets=deetscart,total=total)
        else:
            total=0        
            return render_template('user/index.html',usercart=usercart,cartdeets=deetscart,total=total)




## Create Account Route
@app.route('/customer/account/')
def user_create_account():
    todaysdate=date.today()
    shopping_ID = session.get('user_cart_id')
    
    usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
    deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
        return render_template('user/new_account.html',usercart=usercart,cartdeets=deetscart,total=total)
    else:
        total=0
        return render_template('user/new_account.html',usercart=usercart,cartdeets=deetscart,total=total)
    
    
## Login Route
@app.route('/customer/login/')
def user_login():
    todaysdate=date.today()
    shopping_ID = session.get('user_cart_id')
    
    usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
    deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
        return render_template('user/loginpage.html',usercart=usercart,cartdeets=deetscart,total=total)
    else:
        total=0
        return render_template('user/loginpage.html',usercart=usercart,cartdeets=deetscart,total=total)


## Contact us Route
@app.route('/contact-us/')
def contactus():
    todaysdate=date.today()
    shopping_ID = session.get('user_cart_id')
    
    usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
    deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
    if deetscart!=[]:
        total=0
        for i in deetscart:
            total=total+i.amount
        return render_template('user/contactus.html',usercart=usercart,cartdeets=deetscart,total=total)
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
        

        
## Men Footware Shopping Page
@app.route('/shop/men/')
def shop_men():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        todaysdate=date.today()
        men_footware=db.session.query(Product).filter(Product.product_category=='1').all()
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
        else:
            total=0
        return render_template('user/shopmen.html',MFoot=men_footware,usercart=usercart,cartdeets=deetscart,total=total)
    else:
        return redirect('/customer/account/')
    

## Men Accesories Shopping Page
@app.route('/shop/men/accessories/')
def shop_men_accessories():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        todaysdate=date.today()
        men_accessories=db.session.query(Product).filter(Product.product_category=='2').all()
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
        else:
            total=0
        return render_template('user/male_accessories.html',menAcc=men_accessories,usercart=usercart,cartdeets=deetscart,total=total)
    else:
        return redirect('/customer/account/')
    
    
## Women Shopping Page
@app.route('/shop/women/')
def shop_women():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        todaysdate=date.today()
        women_footware=db.session.query(Product).filter(Product.product_category=='3').all()
        
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
        else:
            total=0
        return render_template('user/shopwomen.html',WFoot=women_footware,usercart=usercart,cartdeets=deetscart,total=total)
    else:
        return redirect('/customer/account/')



## Women Accessories Shopping Page
@app.route('/shop/women/accessories/')
def shop_women_accessores():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        todaysdate=date.today()
        women_accessories=db.session.query(Product).filter(Product.product_category=='4').all()
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        if deetscart!=[]:
            total=0
            for i in deetscart:
                total=total+i.amount
        else:
            total=0
        return render_template('user/female_accessories.html',women_acc=women_accessories,usercart=usercart,cartdeets=deetscart,total=total)
    else:
        return redirect('/customer/account/')


def validate_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return True
    else:
        return False
    
    
## Subscribe Newsletter
@app.route('/subscribe_newsletter/',methods=['POST'])
def reg_newsletter():
    usermail=request.form.get('emailaddress')
    # the_csrf=request.form.get('csrf_token')
    
    if usermail=="":
        return 'Please fill out all fields'
    else:
        email_validation = validate_email(usermail)
        
        if email_validation is True:
            check_email_presence = Newsletter_subscription.query.filter(Newsletter_subscription.email==usermail).first()
            if check_email_presence is None:
                add_to_newsletter = Newsletter_subscription(email = usermail, date_reg=date.today())
                db.session.add(add_to_newsletter)
                db.session.commit()
                return 'Successfully Registered'
            else:
                return 'Email Already Registered'
        else:
            return 'Please provide a valid email'
        
        # if usermail.endswith('@gmail.com'):
        #     with open('newsletter.txt','a')as file:
        #         file.write(f"{usermail} \n")
        #     return 'Successfully Registered'
        # else:
        #     return 'Please provide a valid Google mail account'
        

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
def user_login_verification():
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
                return redirect('/customer/login/')
            
        else:
            flash('Invalid Login Credentials',category='wrong_details')
            return redirect('/customer/login/')
    else:
        flash('Please fill out the form',category='wrong_details')
        return redirect('/customer/login/')


## User Logout Route
@app.route('/customer/logout/')
def user_logout():
    session.pop('user_id',None)
    session.pop('username',None)
    session.pop('user_cart_id',None)
    return redirect('/')




## Add to Cart
@app.route('/add/cart/')
def test():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID != None:
        productid=request.args.get('product')
        quantity=request.args.get('quantity')
        amount_payable=request.args.get('amount')
        user_cart_no=request.args.get('temp_id')
        today_date=date.today()
        
        try:
            add_to_cart=Cart(user_cart_id=user_cart_no, product=productid, product_qty=quantity, amount=amount_payable,cart_date=today_date)
            db.session.add(add_to_cart)
            db.session.commit()
            return "Item Added"
        except:
            return "Something went wrong. Please Try again"
    else:
        return redirect('/')


   
## removecartitem
@app.route('/removeitem/')
def removeitem():
    item2remove=request.args.get('trash')
    
    discard=db.session.query(Cart).get(item2remove)
    db.session.delete(discard)
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


### Update cart quantity
@app.route('/confirm_order/',methods=['POST'])
def confirmOrder():
    if session.get('user_id')!=None and session.get('username')!=None:
        if session.get('user_cart_id')!=None:
            
            total_amount=request.form.get('totalamt')
            cartID=request.form.get('userCartNumber')
            shipping=request.form.get('shipping_address')
            reference=int((random.random() * 1000000000)+1)
            session['txn_ref']=reference
            status='Pending'
            client=session.get("user_id")
            the_order_date=date.today()
            
            ## This adds to the order table
            Ord=Order(buyer=client, ref_no=reference, order_date=the_order_date, order_status=status, order_amount=total_amount, shipping_address=shipping, order_payment='Pending')
            db.session.add(Ord)
            db.session.commit()
            
            
            #to add to order details table
            userOrderId=db.session.query(Order).filter(Order.buyer==session.get('user_id'),Order.ref_no==reference).first()
            
            #this is the order ID
            OrddID=userOrderId.order_id
            
            cartinfo=db.session.query(Cart).filter(Cart.user_cart_id==cartID).all()
            for i in cartinfo:
                Ord_DET=Order_details(order_id=OrddID, prod_id=i.product, product_qty=i.product_qty, prod_price=i.amount)
                db.session.add(Ord_DET)
                #db.session.delete(i)
            db.session.commit()
            
            ## This is to show the customer the info and initialize payment
            orderinfo=db.session.query(Order).filter(Order.ref_no==reference, Order.buyer==session.get('user_id')).first()
            theOrderID=orderinfo.order_id
            theamountPayable=orderinfo.order_amount
            
            orderdeetsinfo=db.session.query(Order_details).filter(Order_details.order_id==theOrderID).all()
            
           
            
            #passing cart info to the route
            todaysdate=date.today()
            usercart=db.session.query(Cart).filter(Cart.user_cart_id==cartID).count()
            deetscart=db.session.query(Cart).filter(Cart.user_cart_id==cartID).all()
            if deetscart!=[]:
                total=0
                for i in deetscart:
                    total=total+i.amount
            else:
                total=0
            return render_template('user/informationpage.html',Ord_Details=orderdeetsinfo, payable=theamountPayable,ref=reference,usercart=usercart,cartdeets=deetscart,total=total)
        else:
            return redirect('/')
    else:
        return redirect('/customer/login/')


## Bad Internet
@app.route('/connection/failed/')
def no_internet():
    session.pop("user_cart_id", None)
    return render_template("user/badinternet.html")


# Order Info Page
@app.route('/call/paystack/')
def paystack():
    if session.get('user_id')!=None and session.get('username')!=None:
        loggedin=session.get('user_id')
        buyerinfo=db.session.query(Customer).get(loggedin)
        
        orderinfo=db.session.query(Order).filter(Order.ref_no==session.get('txn_ref')).first()
        
        
        #writing into payment table
        try:
            pay=Payment(pay_orderid=orderinfo.order_id, pay_amt=orderinfo.order_amount, pay_ref=session.get('txn_ref'), pay_date=datetime.now(), pay_status="Pending", pay_feedback='Pending')
            db.session.add(pay)
            db.session.commit()
        except:
            the_duplicate=db.session.query(Payment).filter(Payment.pay_ref==session.get('txn_ref')).first()
            db.session.delete(the_duplicate)
            
            pay=Payment(pay_orderid=orderinfo.order_id, pay_amt=orderinfo.order_amount, pay_ref=session.get('txn_ref'), pay_date=datetime.now(), pay_status="Pending", pay_feedback='Pending')
            db.session.add(pay)
            db.session.commit()
        
        #here we send info to paystack
        data = {
            "email":buyerinfo.cust_email,
            "amount":orderinfo.order_amount*100, 
            "reference":session.get('txn_ref')
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization":"Bearer sk_test_2d885e99a5f8c0ca434f5862d78a5de5603962cd"
        }
        
        try:
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
            
            if rsp_json['status'] == True and rsp_json['message']=="Authorization URL created":
                url = rsp_json['data']['authorization_url']
                
                #delete cart items 
                cartitems=db.session.query(Cart).filter(Cart.user_cart_id==session.get('user_cart_id')).all()
                for cart in cartitems:
                    db.session.delete(cart)
                db.session.commit()
                
                
                # pop the cart id session
                session.pop('user_cart_id',None)
                
                return redirect(url)
        except:
            #discard payment record
            discard_payment=db.session.query(Payment).filter(Payment.pay_ref==session.get('txn_ref')).first()
            order_request_id=discard_payment.pay_orderid
            
            db.session.delete(discard_payment)
            
            #delete order_details record
            discard_ord_details=db.session.query(Order_details).filter(Order_details.order_id==order_request_id).all()
            for i in discard_ord_details:
                db.session.delete(i)
            
            
            # update order record
            update_order=db.session.query(Order).get(order_request_id)
            update_order.order_status='Network Failed'
            update_order.order_payment='Failed'
            
            #delete cart details
            cartitems=db.session.query(Cart).filter(Cart.user_cart_id==session.get('user_cart_id')).all()
            for cart in cartitems:
                db.session.delete(cart)
            db.session.commit()
                
            # pop the cart id session
            session.pop('user_cart_id',None)
            
            return redirect('/connection/failed/')
    else:
        return redirect('/customer/account/')
 
 
 
   
## Second API consumption phase. Transaction Verification Phase
@app.route('/paystack_landing/')
def paystack_landing():
    """This route would have been configured in the paystack developer dashboard, this is where user would be redirected to after inputing their card details, here you will confirm the transaction status and update your db accordingly"""

    if session.get('user_id')!=None and session.get('username')!=None:
        loggedin = session.get('user_id')
        ref = session.get('txn_ref')
        pay_ord_id = Payment.query.filter(Payment.pay_ref==ref).first()
        pOID=pay_ord_id.pay_orderid
        
        headers = {
            "Content-Type": "application/json",
            "Authorization":"Bearer sk_test_2d885e99a5f8c0ca434f5862d78a5de5603962cd"
        }
        
        response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
        rsp_json = response.json() 
        
        customerdeets=db.session.query(Customer).get(loggedin)
        
        if rsp_json['status'] == True: 
            data = rsp_json['data']
            actual_amt = data['amount']/100
            feedback = data['gateway_response']
            
            # update order record
            update_order=db.session.query(Order).get(pOID)
            update_order.order_payment='Paid'
            
            #update payment table
            pay = Payment.query.filter(Payment.pay_ref==ref).first()
            pay.pay_status = 'Paid'
            pay.pay_feedback =feedback
            db.session.commit()
            
            return render_template('user/txn_success.html',customer=f'{customerdeets.cust_firstname} {customerdeets.cust_lastname}', trn_ref=ref, currency=data['currency'], amount=actual_amt, day_of_txn=date.today())
        else:
            data = rsp_json['data']
            actual_amt = data['amount']/100
            feedback = data['gateway_response']
            
            # update order record
            update_order=db.session.query(Order).get(pOID)
            update_order.order_payment='Failed'
            
            #update payment table
            pay = Payment.query.filter(Payment.pay_ref==ref).first()
            pay.pay_status = 'Failed'
            pay.pay_feedback ='Transaction Failed'
            db.session.commit()
            
            return render_template('user/txn_failed.html',customer=f'{customerdeets.cust_firstname} {customerdeets.cust_lastname}', trn_ref=ref, currency=data['currency'], amount=actual_amt, day_of_txn=date.today())
    else:
        return redirect('/customer/account/')



### ERROR 404 and 500 Pages
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('user/chrisllan500error.html',error=error),500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('user/chrisllan404error.html',error=error),404



# Track Order View
@app.route('/track-orders/')
def track_orders():
    if session.get('user_id') !=None and session.get('username') != None:
        todaysdate=date.today()
        shopping_ID = session.get('user_cart_id')
        
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        
        #getting the customer order history
        order_history=db.session.query(Order).filter(Order.buyer==session.get('user_id')).order_by(Order.order_date.desc()).all()
        
        if deetscart != []:
            total=0
            for i in deetscart:
                total=total+i.amount
            return render_template('user/trackorders.html', usercart=usercart, cartdeets=deetscart, total=total, order_history=order_history)
        else:
            total=0
            return render_template('user/trackorders.html', usercart=usercart, cartdeets=deetscart, total=total, order_history=order_history)
    else:
        return redirect('/customer/login/')
    
# customer order details
@app.route('/customer/orderdetails/<id>')
def customer_order_details(id):
    if session.get('user_id') !=None and session.get('username') != None:
        todaysdate=date.today()
        shopping_ID = session.get('user_cart_id')
        
        usercart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).count()
        deetscart=db.session.query(Cart).filter(Cart.user_cart_id==shopping_ID).all()
        
        
        order_deets=db.session.query(Order_details).filter(Order_details.order_id==id).all()
        
        order=db.session.query(Order).filter(Order.order_id==id).first()
        
        if deetscart != []:
            total=0
            for i in deetscart:
                total=total+i.amount
            return render_template('user/trackorderdetails.html', usercart=usercart, cartdeets=deetscart, total=total, order_deets=order_deets, order=order)
        else:
            total=0
            return render_template('user/trackorderdetails.html', usercart=usercart, cartdeets=deetscart, total=total, order_deets=order_deets, order=order)
    else:
        return redirect('/customer/login/')