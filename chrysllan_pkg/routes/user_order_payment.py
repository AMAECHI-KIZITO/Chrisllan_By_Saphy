import requests, json
from datetime import date, datetime
from flask import render_template, session, redirect
from flask_mail import Message
from chrysllan_pkg import app, db, mail
from chrysllan_pkg.models import *

def send_order_email(recipient, username, order_id, total_amount):
    details_of_order = db.session.query(Order_details).filter(Order_details.order_id==order_id).all()
    
    msg = Message("Your Chrisllan by Saphy Order Has Been Placed", sender=('Chrisllan By Saphy', 'konkakira1960@gmail.com'), recipients=[recipient])
    msg.html = render_template('order_placed.html', recipient=recipient, username=username, year=date.today().year, order_details=details_of_order, amount=total_amount)
    mail.send(msg)
    return 200
     
     
     
@app.route('/cancel-order/<order_id>')
def cancel_order(order_id):     
    order_info = Order.query.get(order_id)
    customer_deets = Customer.query.get(order_info.buyer)
    order_info.order_status = 'Cancelled'
    order_info.order_payment = 'Cancelled'
    db.session.commit()
    return render_template("user/order_cancelled.html", customer=f'{customer_deets.cust_firstname} {customer_deets.cust_lastname}', trn_ref=order_info.ref_no, amount=order_info.order_amount, day_of_txn = date.today())

# Process payment
@app.route('/proceed-to-payment/')
def pay_for_order():
    if session.get('user_id')!=None and session.get('username')!=None:
        loggedin = session.get('user_id')
        buyerinfo = db.session.query(Customer).get(loggedin)
        orderinfo = db.session.query(Order).filter(Order.ref_no==session.get('txn_ref')).first()
        
        #writing into payment table
        try:
            new_payment_record = Payment(pay_orderid=orderinfo.order_id, pay_amt=orderinfo.order_amount, pay_ref=session.get('txn_ref'), pay_date=datetime.now(), pay_status="Pending", pay_feedback='Pending')
            db.session.add(new_payment_record)
            db.session.commit()
        except:
            the_duplicate=db.session.query(Payment).filter(Payment.pay_ref==session.get('txn_ref')).first()
            db.session.delete(the_duplicate)
            
            new_payment_record = Payment(pay_orderid=orderinfo.order_id, pay_amt=orderinfo.order_amount, pay_ref=session.get('txn_ref'), pay_date=datetime.now(), pay_status="Pending", pay_feedback='Pending')
            db.session.add(new_payment_record)
            db.session.commit()
        
        
        data = {
            "email": buyerinfo.cust_email,
            "amount": orderinfo.order_amount * 100, 
            "reference": session.get('txn_ref'),
            "metadata": {
                "cancel_action": f"http://127.0.0.1:8700/cancel-order/{orderinfo.order_id}"
            },
            "callback_url":"http://127.0.0.1:8700/verify-payment/"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization":"Bearer sk_test_2d885e99a5f8c0ca434f5862d78a5de5603962cd"
        }
        
        try:
            response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, data=json.dumps(data))
            rsp_json = response.json()
            
            if rsp_json['status'] == True and rsp_json['message'] == "Authorization URL created":
                url = rsp_json['data']['authorization_url']
                
                #delete cart items 
                cartitems = db.session.query(Cart).filter(Cart.user_cart_id==session.get('user_cart_id')).all()
                for cart in cartitems:
                    db.session.delete(cart)
                db.session.commit()
                
                # pop the cart id session
                # session.pop('user_cart_id', None)
                
                return redirect(url)
            else:
                return "Seems like the payment failed"
        except:
            #discard payment record
            discard_payment = db.session.query(Payment).filter(Payment.pay_ref==session.get('txn_ref')).first()
            order_request_id = discard_payment.pay_orderid
            
            db.session.delete(discard_payment)
            
            #delete order_details record
            # discard_ord_details=db.session.query(Order_details).filter(Order_details.order_id==order_request_id).all()
            # for i in discard_ord_details:
            #     db.session.delete(i)
            
            
            # update order record
            update_order=db.session.query(Order).get(order_request_id)
            update_order.order_status='Network Failed'
            update_order.order_payment='Failed'
            
            #delete cart details
            # cartitems=db.session.query(Cart).filter(Cart.user_cart_id==session.get('user_cart_id')).all()
            # for cart in cartitems:
            #     db.session.delete(cart)
            # db.session.commit()
                
            # pop the cart id session
            # session.pop('user_cart_id',None)
            
            return redirect('/connection/failed/')
    else:
        return redirect('/customer/account/')
 
 
 
   
## Transaction Verification Phase
@app.route('/verify-payment/')
def paystack_landing():
    if session.get('user_id')!=None and session.get('username')!=None:
        loggedin = session.get('user_id')
        ref = session.get('txn_ref')
        pay_ord_id = Payment.query.filter(Payment.pay_ref==ref).first()
        pOID = pay_ord_id.pay_orderid
        
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
            pay.pay_feedback = feedback
            db.session.commit()
            
            
            
            inform_customer = send_order_email(customerdeets.cust_email, customerdeets.cust_firstname, pOID, actual_amt)
            
            return render_template('user/txn_success.html', customer=f'{customerdeets.cust_firstname} {customerdeets.cust_lastname}', trn_ref=ref, currency=data['currency'], amount=actual_amt, day_of_txn=date.today())
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
