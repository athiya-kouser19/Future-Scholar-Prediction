from flask import Flask, request, render_template, redirect, session, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model_path = 'd:/phase1/predict/Getting-Admission-in-College-Prediction-main/linear_regression_model.pkl'
model = joblib.load(model_path)

app.secret_key = 'secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index1')
def index1():
    return render_template('index1.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_users WHERE email=%s AND password=%s', (email, password,))
        tbl_users = cursor.fetchone()
        if tbl_users:
            session['loggedin'] = True
            session['email'] = tbl_users['email']
            session['password'] = tbl_users['password']
            return render_template('dashboard.html', message="Logged in successfully")
        else:
            return render_template('login.html', error="Invalid email or password")
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_users WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO tbl_users (username, email, password) VALUES (%s, %s, %s)', (userName, email, password,))
            mysql.connection.commit()
            message = 'You have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        gre = float(request.form['gre'])
        toefl = float(request.form['toefl'])
        university_rating = float(request.form['university_rating'])
        sop = float(request.form['sop'])
        lor = float(request.form['lor'])
        cgpa = float(request.form['cgpa'])
        research = float(request.form['research'])
        
        prediction = model.predict([[gre, toefl, university_rating, sop, lor, cgpa, research]])
        output = round(prediction[0], 3) * 100
        
        if output >= 90:
            colleges = [
                {'name': 'Massachusetts Institute of Technology (MIT) ', 'location': 'United States'},
                {'name': 'Imperial College London ', 'location': 'United Kingdom'}
            ]
        elif output >= 80:
            colleges = [
                {'name': 'University of Oxford ', 'location': 'united kingdom'},
                {'name': 'Harvard University ', 'location': 'united state'}
            ]
        elif output >= 75:
            colleges = [
                {'name': 'University of Cambridge ', 'location': 'UK'},
                {'name': 'ETH Zurich (Swiss Federal Institute of Technology) ', 'location': 'Switzerland '}
            ]
        else:
            colleges = [
                {'name': 'National University of Singapore (NUS)', 'location': 'Singapore'},
                {'name': 'UCL (University College London) ', 'location': 'UK'}
            ]
        
        return render_template('result.html', prediction_text=f'Probability of admission: {output}%', colleges=colleges)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
