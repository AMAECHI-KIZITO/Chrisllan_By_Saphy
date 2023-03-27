from datetime import date
from flask import render_template,redirect,session,request,flash
from werkzeug.security import check_password_hash
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *

@app.route('/admin/')
def admin_login():
    return render_template('admin/admin_login.html')


## ADMIN VERIFY LOGIN       
@app.route('/admin/login/',methods=['POST'])
def admin_verify_login():
    admin_email=request.form.get('admin_email')
    admin_pswd=request.form.get('admin_pswd')
    
    admin_record = db.session.query(Admin).filter(Admin.admin_email==admin_email).first()
    if admin_record and check_password_hash(admin_record.admin_pswd, admin_pswd):
        session['admin_name']=admin_record.admin_firstname
        session['admin_id']=admin_record.admin_id
        day=date.today()
        totalcust=db.session.query(Customer).count()
        totalorders=db.session.query(Order).filter(Order.order_payment=='Paid').count()
        todayorder=db.session.query(Order).filter(Order.order_date==day).count()
        totalincome = db.session.query(Order).filter(Order.order_payment=='Paid').all()
        
        revenue = 0
        if totalincome != []:
            for i in totalincome:
                revenue = revenue + i.order_amount
            return render_template('admin/admindashboard.html',cust=totalcust, allorder=totalorders, todayorder=todayorder, revenue=revenue)
        else:
            return render_template('admin/admindashboard.html',cust=totalcust, allorder=totalorders, todayorder=todayorder, revenue=revenue)
    else:
        flash('Incorrect Credentials', category='wrong_admin_login')
        return redirect('/admin/')
    
    
@app.route('/admin/logout/')
def admin_logout():
    session.pop('admin_name',None)
    session.pop('admin_id',None)
    return redirect('/admin/')