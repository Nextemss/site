from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_from_directory
import os 
from os import path
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import random
import shutil
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'
db = SQLAlchemy(app)

words = ["think slow decide fast", "move and grow", "lead the world to progress"]
endw = ['download']



















class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def check_password(self, password):
        return self.password == password

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(50))
    description = db.Column(db.String(200))

    def __init__(self, file_name, description):
        self.file_name = file_name
        self.description = description

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('log.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('log.html')

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return render_template('log.html')


        session['user_id'] = user.id
        session['username'] = user.username  
        return redirect(url_for('home'))

    return render_template('log.html')




@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
    

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = session.get('username', '')  
    return render_template('profile.html', username=username)




@app.route('/home')
@login_required
def home():
    files = Project.query.all()
    username = session.get('username', '')  

    if len(username) > 8:
        username = username[:8] + "..."  
    files = os.listdir('C:/Users/Nextems/Documents/project/progga')
    return render_template('main.html', username=username, word=random.choice(words), file_names=files)



if not os.path.exists('progga'):
    os.makedirs('progga') 





@app.route('/descriptions', methods=['GET', 'POST'])
@login_required
def descriptions():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename

            description = request.form.get('description')
           
            file_name = filename
            project = Project(file_name=file_name, description=description)
            db.session.add(project)
            db.session.commit()

         
            file_path = os.path.join('C:/Users/Nextems/Documents/project/progga', filename)
            file.save(file_path)

            return redirect(url_for('home'))
    files = os.listdir('C:/Users/Nextems/Documents/project/progga')
    return render_template('main.html', file_names=files)



@app.route('/download/<file_names>', methods=['GET', 'POST'])
@login_required
def download_file(file_names):
    directory = os.path.abspath('C:/Users/Nextems/Documents/project/progga') 
    return send_from_directory(directory, file_names, as_attachment=True)






@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not username or not password or not email:
            return render_template('log.html')

        if User.query.filter_by(username=username).first():
            return render_template('log.html')

        if User.query.filter_by(email=email).first():
            return render_template('log.html')

        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()

       
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('home'))

    return render_template('log.html')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
