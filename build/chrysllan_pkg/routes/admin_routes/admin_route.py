from datetime import date
from flask import render_template, redirect, session, request, flash
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

      
## Admin Home Dashboard
@app.route('/admin/dashboard/')
def admin_Home():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        day=date.today()
        totalcust = db.session.query(Customer).count()
        totalorders = db.session.query(Order).filter(Order.order_payment=='Paid').count()
        todayorder = db.session.query(Order).filter(Order.order_date==day).count()
        totalincome = db.session.query(Order).filter(Order.order_payment=='Paid').all()
        
        revenue = 0
        if totalincome != []:
            for i in totalincome:
                revenue = revenue + i.order_amount
            return render_template('admin/admindashboard.html',cust=totalcust, allorder=totalorders, todayorder=todayorder, revenue=revenue)
        else:
            return render_template('admin/admindashboard.html',cust=totalcust, allorder=totalorders, todayorder=todayorder, revenue=revenue)
    else:
        return redirect('/admin/')
    
    
@app.after_request
def clearcache(response):
    response.headers['Cache-Control']="no-cache, no store, must-revalidate"
    return response



    
    
