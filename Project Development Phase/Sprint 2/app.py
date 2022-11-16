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

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['email']
        password = request.form['password']
        option = request.form.get('role',False)
        msg="Selected"+option
        print(option)
        if option=="Retailer":
            sql = "SELECT * FROM RETAILERS WHERE email =? AND password=?"
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
                return render_template('login.html', msg = msg)
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
                session['username'] = account['USERNAME']
                msg = 'Logged in successfully !'
                print(session['loggedin'])
                return render_template('login.html', msg = msg)
            else:
                msg = 'Incorrect username / password !'
   
    return render_template('login_form.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def welcome():
    msg=""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        option = request.form.get('role',False)
        msg="Selected"+option
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
     #   else:
      #      return render_template('retailerhomepg.html')
    return render_template('registration_form.html',msg=msg)
       
if __name__ == '__main__':
   #app.run(host='0.0.0.0')
   app.run(debug = True)
