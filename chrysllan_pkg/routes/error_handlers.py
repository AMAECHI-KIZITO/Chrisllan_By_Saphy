from datetime import date
from flask import render_template, session
from chrysllan_pkg import app,db
from chrysllan_pkg.models import *


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('user/chrisllan500error.html', error=error), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('user/chrisllan404error.html', error=error), 404

@app.errorhandler(413)
def file_too_large(error):
    return 'File too large. Max file upload size is 5mb', 413

## Bad Internet
@app.route('/connection/failed/')
def no_internet():
    session.pop("user_cart_id", None)
    return render_template("user/badinternet.html")