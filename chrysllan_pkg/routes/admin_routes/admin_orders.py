from datetime import date
from flask import render_template, redirect, session, request, flash
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

## All Orders
@app.route('/admin/all-orders/')
def all_orders():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        allorders=db.session.query(Order).filter(Order.order_payment=='Paid').order_by(Order.order_date.desc()).all()
        return render_template('admin/allorders.html',allorders=allorders)
    else:
        return redirect('/admin/')
    
    
## View Orders
@app.route('/vieworder/<id>')
def view_order_details(id):
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        specific=db.session.query(Order_details).filter(Order_details.order_id==id).all()
        order=db.session.query(Order).filter(Order.order_id==id).first()
        amt=order.order_amount
        return render_template('admin/vieworder.html', specific=specific, id=id, amt=amt, order=order)
    else:
        return redirect('/admin/')
    
## Update Order Status
@app.route('/update-order-status/<id>', methods=['POST'])
def update_order_status(id):
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        specific=db.session.query(Order).filter(Order.order_id==id).first()
        specific.order_status='Completed'
        db.session.commit()
        return redirect('/admin/all-orders/')
    else:
        return redirect('/admin/')
    