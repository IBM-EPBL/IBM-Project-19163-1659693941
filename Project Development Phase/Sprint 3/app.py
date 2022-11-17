from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import ibm_db
import re

app = Flask(__name__,static_url_path="")
            
#static_folder="C:/Users/Bhuvaneswari/Desktop/cad/new/Final_project/static");
  
app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tbl66129;PWD=LPzyHjRGcmXprQoN",'','')

@app.route('/',methods =['GET', 'POST'])

def homer():
    return render_template('Inventory_Homepage.html');

@app.route('/terms',methods =['GET', 'POST'])
def terms():
    return render_template('terms_and_conditions_page.html');

@app.route('/aboutus',methods =['GET', 'POST'])
def about():
    return render_template('aboutus.html');

@app.route('/services',methods =['GET', 'POST'])
def services():
    return render_template('services.html');


@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['email']
        password = request.form['password']
        option = request.form.get('role')
        msg="Selected"+option
        print(option)
        if option=="Retailer":
            sql = "SELECT * FROM RETAILER WHERE email =? AND password=?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,username)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print (account)
            if account:
                #print("hi")
                session['loggedin'] = True
                session['id'] = account['EMAIL']
                userid=  account['EMAIL']
                session['username'] = account['EMAIL']
                msg = 'Logged in successfully !'
                print(session['loggedin'])
                return render_template('Inventory_Homepage.html', msg = msg)
            else:
                msg = 'Incorrect username / password !'
        elif option=="Customer":
            sql = "SELECT * FROM CUSTOMER WHERE email =? AND password=?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,username)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print (account)
            if account:
                #print("hi")
                session['loggedin'] = True
                session['id'] = account['EMAIL']
                userid=  account['EMAIL']
                session['username'] = account['EMAIL']
                msg = 'Logged in successfully !'
                print(session['loggedin'])
                return render_template('products.html', msg = msg)
            else:
                msg = 'Incorrect username / password !'
    
    return render_template('login_form.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def welcome():
    msg=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        option = request.form['role']
        #msg="Selected"+ option
        print(option)
        if option=="Customer":
            sql = "SELECT * FROM CUSTOMER WHERE EMAIL =?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print(account)
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[0-9]+', phone):
                msg = 'name must contain only numbers !'
            else:
                insert_sql = "INSERT INTO CUSTOMER (EMAIL,PASSWORD,PHONE) VALUES (?,?,?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, email)
                ibm_db.bind_param(prep_stmt, 2, password)
                ibm_db.bind_param(prep_stmt, 3, phone)
                ibm_db.execute(prep_stmt)
                msg = 'You have successfully registered !'
                return render_template('Inventory_Homepage.html')
        elif option=="Retailer":
            sql = "SELECT * FROM RETAILER WHERE EMAIL =?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print(account)
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[0-9]+', phone):
                msg = 'name must contain only numbers !'
            else:
                insert_sql = "INSERT INTO RETAILER (EMAIL,PASSWORD,PHONE) VALUES (?,?,?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt,1, email)
                ibm_db.bind_param(prep_stmt, 2, password)
                ibm_db.bind_param(prep_stmt, 3, phone)
                ibm_db.execute(prep_stmt)
                msg = 'You have successfully registered !'
                return render_template('Inventory_Homepage.html')
            
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
            return render_template('registration_form.html')
     
    return render_template('registration_form.html',msg=msg)

@app.route('/vendoradd', methods =['GET', 'POST'])
def vadd():
    msg=""
    if request.method == "POST":
        vid = request.form['vid']
        vname = request.form['vname']
        pid = request.form['pid']
        option = request.form.get('catg',False)
        msg="Selected"+option
        print(option)
        sql = "SELECT * FROM VENDORS WHERE VENDOR_ID = ?" 
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,vid)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
           
        else:
            insert_sql = "INSERT INTO VENDORS (VENDOR_ID,VENDOR_NAME,CATEGORY,PRODUCTID) VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, vid)
            ibm_db.bind_param(prep_stmt, 2, vname)
            ibm_db.bind_param(prep_stmt, 3, option)
            ibm_db.bind_param(prep_stmt, 4, pid)
            ibm_db.execute(prep_stmt)
            msg = 'Successfully added !'
            return render_template('Inventory_Homepage.html')
        
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
            return render_template('vendoradd.html')
     
    return render_template('vendoradd.html',msg=msg)

@app.route('/vendorupdate', methods =['GET', 'POST'])
def vupdate():
    msg=""
    if request.method == "POST":
        vid = request.form['vid']
        vname = request.form['vname']
        pid = request.form['pid']
        option = request.form.get('catg',False)
        msg="Selected"+option
        print(option)
        sql = "SELECT * FROM VENDORS WHERE VENDOR_ID = ?" 
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,vid)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            insert_sql = "UPDATE TBL66129.VENDORS SET VENDOR_NAME = ?,CATEGORY=?,PRODUCTID=? WHERE VENDOR_ID=?"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, vname)
            ibm_db.bind_param(prep_stmt, 2, option)
            ibm_db.bind_param(prep_stmt, 3, pid)
            ibm_db.bind_param(prep_stmt, 4, vid)
            ibm_db.execute(prep_stmt)
            msg = 'Successfully updated !'
            return render_template('Inventory_Homepage.html')
        
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
            return render_template('vendorupdate.html')
     
    return render_template('vendorupdate.html',msg=msg)

@app.route('/vendordel', methods =['GET', 'POST'])
def vdel():
    msg=""
    if request.method == "POST":
        vid = request.form['vid']
        sql = "SELECT * FROM VENDORS WHERE VENDOR_ID = ?" 
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,vid)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            insert_sql = "DELETE FROM VENDORS WHERE VENDOR_ID=?"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, vid)
            ibm_db.execute(prep_stmt)
            msg = 'Successfully deleted !'
            return render_template('Inventory_Homepage.html')
        
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
            return render_template('vendordel.html')
     
    return render_template('vendordel.html',msg=msg)

@app.route('/productadd', methods =['GET', 'POST'])
def padd():
    msg=""
    if request.method == "POST":
        pid = request.form['pid']
        pname = request.form['pname']
        vid = request.form['vid']
        pr = request.form['pr']
        qty = request.form['qty']
        desc = request.form['desc']
        option = request.form.get('catg',False)
        msg="Selected"+option
        print(option)
        sql = "SELECT * FROM PRODUCTS WHERE PRODUCTID = ?" 
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,pid)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
           
        else:
            insert_sql = "INSERT INTO PRODUCTS VALUES (?,?,?,?,?,?,?)"
            #(VENDOR_ID,VENDOR_NAME,CATEGORY,PRODUCTID)
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, pid)
            ibm_db.bind_param(prep_stmt, 2, pname)
            ibm_db.bind_param(prep_stmt, 3, pr)
            ibm_db.bind_param(prep_stmt, 4, option)
            ibm_db.bind_param(prep_stmt, 5, vid)
            ibm_db.bind_param(prep_stmt, 6, qty)
            ibm_db.bind_param(prep_stmt, 7, desc)
            ibm_db.execute(prep_stmt)
            msg = 'Successfully added !'
            return render_template('Inventory_Homepage.html')
        
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
            return render_template('productadd.html')
     
    return render_template('productadd.html',msg=msg)

@app.route('/productupdate', methods =['GET', 'POST'])
def pdupdate():
    msg=""
    if request.method == "POST":
        pid = request.form['pid']
        pname = request.form['pname']
        vid = request.form['vid']
        pr = request.form['pr']
        qty = request.form['qty']
        desc = request.form['desc']
        option = request.form.get('catg',False)
        msg="Selected"+option
        print(option)
        sql = "SELECT * FROM PRODUCTS WHERE PRODUCTID = ?" 
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,pid)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            insert_sql = "UPDATE TBL66129.PRODUCTS SET PRODUCT_NAME = ?,PRICE = ?,CATEGORY = ?, VENDOR_ID = ?, QUANTITY = ?, DESCRIPTION = ? WHERE PRODUCTID = ?"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, pname)
            ibm_db.bind_param(prep_stmt, 2, pr)
            ibm_db.bind_param(prep_stmt, 3, option)
            ibm_db.bind_param(prep_stmt, 4, vid)
            ibm_db.bind_param(prep_stmt, 5, qty)
            ibm_db.bind_param(prep_stmt, 6, desc)
            ibm_db.bind_param(prep_stmt, 7, pid)
            ibm_db.execute(prep_stmt)
            msg = 'Successfully updated !'
            return render_template('Inventory_Homepage.html')
        
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
            return render_template('productupdate.html')
     
    return render_template('productupdate.html',msg=msg)

@app.route('/productdel', methods =['GET', 'POST'])
def pdel():
    msg=""
    if request.method == "POST":
        pid = request.form['pid']
        sql = "SELECT * FROM PRODUCTS WHERE PRODUCTID = ?" 
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,pid)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            insert_sql = "DELETE FROM PRODUCTS WHERE PRODUCTID=?"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, pid)
            ibm_db.execute(prep_stmt)
            msg = 'Successfully deleted !'
            return render_template('Inventory_Homepage.html')
        
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
            return render_template('productdel.html')
     
    return render_template('productdel.html',msg=msg)

@app.route('/display')
def display():
    msg=""
    #print(session["username"],session['id'])
    cursor = mysql.connection.cursor()
    #cursor.execute('SELECT * FROM job WHERE userid = % s', (session['id'],))
    
    #print("accountdislay",account)
    #cursor = conn.cursor()
    cursor.execute("SELECT * FROM TBL66129.PRODUCTS")
    #account = cursor.fetchone()
    for r in cursor.fetchall():
        print(r)
    return render_template('display.html',msg=r)

       
if __name__ == '__main__':
   #app.run(host='0.0.0.0')
   app.run(debug = True)
