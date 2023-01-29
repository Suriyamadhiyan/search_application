from flask import Flask, render_template, request, session, redirect,jsonify
from flask_session import Session
import uuid as uuid
import csv
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="intern"
)
cursor = mydb.cursor()

app = Flask(__name__, template_folder='templates')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/home')
    return render_template('index.html')

#login_validation
@app.route('/login', methods=['POST'])

def login():

    username = request.form['username']

    password = request.form['password']

    # Validate the username and password

    if username == 'user' and password == 'password':

        session_id = str(uuid.uuid4())#session id creation
        session['username'] = request.form['username']
        return redirect('/home')
    else:

        return 'Invalid username or password', 401
    
#redirection
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/')
    return render_template('home.html', username=session['username'])

#keyword_search
@app.route('/home', methods=['POST'])

def search():
    option=request.form['search-criteria']
    value = request.form['search-term']#getting the search result
    results = []

    # Validate the session ID

    if 'username' in session:
        
        if option =='keyword':
            query = "SELECT * FROM product where name= %s"
            cursor.execute(query, (value,))
                   
        elif option =='category':
            query = "SELECT * FROM product where category= %s"
            cursor.execute(query, (value,))
        
        elif option == 'location':
            query = "SELECT * FROM product where location= %s"
            cursor.execute(query, (value,))
        product = cursor.fetchall()
        for result in product:
            results.append(result)
        #return jsonify(results)
        return render_template('home.html', results=results)
    else:
            return 'Invalid session', 401

#logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
