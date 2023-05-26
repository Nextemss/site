from flask import Flask, flash, request, jsonify, render_template, session, redirect, url_for, send_from_directory
import os 
from os import path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from functools import wraps
import random
import shutil
from werkzeug.utils import secure_filename
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'
db = SQLAlchemy(app)

words = ["think slow decide fast", "move and grow", "lead the world to progress"]
endw = ['download']
app.static_folder = 'static'

error = ("no more than 19 characters in the name")






class User(db.Model):
    id = Column(Integer, primary_key=True)  # Идентификатор пользователя (первичный ключ)
    username = Column(String(50), unique=True)  # Имя пользователя (уникальное поле)
    password = Column(String(50))  # Пароль пользователя
    email = Column(String(50), unique=True)  # Email пользователя (уникальное поле)
    date_of_birth = Column(DateTime)  # Дата рождения пользователя
    photo_filename = Column(String(100))  # Имя файла фотографии пользователя

    def __init__(self, username, password, email, date_of_birth):
        # Инициализация объекта User с заданными значениями
        self.username = username  # Имя пользователя
        self.password = password  # Пароль пользователя
        self.email = email  # Email пользователя
        self.date_of_birth = date_of_birth  # Дата рождения пользователя

    def check_password(self, password):
        # Проверка соответствия заданного пароля паролю пользователя
        return self.password == password



class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Идентификатор проекта (первичный ключ)
    file_name = db.Column(db.String(50))  # Имя файла проекта
    description = db.Column(db.String(200))  # Описание проекта

    def __init__(self, file_name, description):
        # Инициализация объекта Project с заданными значениями
        self.file_name = file_name  # Имя файла проекта
        self.description = description  # Описание проекта
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Если идентификатор пользователя не присутствует в сессии,
            # перенаправляем на страницу входа в систему
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    # Маршрут для главной страницы
    return render_template('log.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            # Если имя пользователя или пароль отсутствуют,
            # возвращаем шаблон страницы входа
            return render_template('log.html')

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            # Если пользователь не существует или пароль неверен,
            # возвращаем шаблон страницы входа
            return render_template('log.html')

        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('home'))

    return render_template('log.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Удаляем идентификатор пользователя из сессии
    session.pop('user_id', None)
    
    # Перенаправляем на маршрут 'login'
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Получаем имя пользователя из сессии
    username = session.get('username', '')

    # Получаем объект пользователя из базы данных
    user = User.query.filter_by(username=username).first()

    # Возвращаем шаблон 'profile.html' и передаем в него переменные
    return render_template('profile.html', username=username, date_of_birth=user.date_of_birth, user=user)



@app.route('/home')
@login_required
def home():
    # Получаем список всех проектов из базы данных
    files = Project.query.all()

    # Получаем имя пользователя из сессии
    username = session.get('username', '')

    # Получаем объект пользователя из базы данных
    user = User.query.filter_by(username=username).first()

    # Ограничиваем длину имени пользователя, если оно превышает 8 символов
    if len(username) > 8:
        username = username[:8] + "..."

    # Получаем список имен файлов в директории
    files = os.listdir('C:/Users/Nextems/Documents/project/progga')

    # Возвращаем шаблон 'main.html' и передаем в него переменные
    return render_template('main.html', username=username, word=random.choice(words), file_names=files, date_of_birth=user.date_of_birth, user=user)


# Если директория 'progga' не существует, создаем ее
if not os.path.exists('progga'):
    os.makedirs('progga')


@app.route('/descriptions', methods=['GET', 'POST'])
@login_required
def descriptions():
    # Проверяем метод POST
    if request.method == 'POST':
        # Получаем файл из запроса
        file = request.files['file']
        if file:
            # Получаем данные из формы
            filename = file.filename
            description = request.form.get('description')
            file_name = filename
            
            # Создаем новый объект проекта с именем файла и описанием
            project = Project(file_name=file_name, description=description)
            
            # Добавляем проект в сеанс базы данных и сохраняем изменения
            db.session.add(project)
            db.session.commit()

            # Сохраняем файл в указанную директорию
            file_path = os.path.join('C:/Users/Nextems/Documents/project/progga', filename)
            file.save(file_path)

            # Перенаправляем на маршрут 'home'
            return redirect(url_for('home'))
    
    # Получаем список имен файлов в директории
    files = os.listdir('C:/Users/Nextems/Documents/project/progga')
    
    #передаем имена файлов в качестве переменной
    return render_template('main.html', file_names=files)



@app.route('/download/<file_names>', methods=['GET', 'POST'])
@login_required
def download_file(file_names):
    #Получаем дирикторию установки с сервера
    directory = os.path.abspath('C:/Users/Nextems/Documents/project/progga') 
    return send_from_directory(directory, file_names, as_attachment=True)





@app.route('/register', methods=['GET', 'POST'])
def register():
    # Проверяем метод POST
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        day = int(request.form.get('day'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))

        # Проверяем, что все поля заполнены
        if not username or not password or not email:
            return render_template('log.html')

        # Проверяем, что пользователь с таким именем не существует
        if User.query.filter_by(username=username).first():
            return render_template('log.html')


        # Проверяем, что длина имени пользователя не превышает 19 символов
        if len(username) > 19:
            return render_template('log.html', error)



        # Проверяем, что пользователь с такой почтой не существует
        if User.query.filter_by(email=email).first():
            return render_template('log.html')

        # Создаем объект User с полученными данными
        dob = datetime(year, month, day)
        user = User(username=username, password=password, email=email, date_of_birth=dob)
        db.session.add(user)
        db.session.commit()

        # Устанавливаем данные пользователя в сессии
        session['user_id'] = user.id
        session['username'] = user.username

        # Перенаправляем на маршрут 'home'
        return redirect(url_for('home'))

    # Возвращаем шаблон 'log.html' для GET-запроса
    return render_template('log.html')



@app.route('/avatar', methods=['POST'])
@login_required
def upload_avatar():
    username = session.get('username', '')
    user = User.query.filter_by(username=username).first()

    # Проверяем, загружен ли файл
    if 'file' not in request.files:
        flash('Файл не найден')
        return redirect('/profile')

    file = request.files['file']

    # Если пользователь не выбрал файл, то браузер отправляет пустой файл
    if file.filename == '':
        flash('Файл не выбран')
        return redirect('/profile')

    if file:
        avatar_folder = 'C:/Users/Nextems/Documents/project/static/avatar'

        # Удаляем существующий файл фотографии, если он есть
        if user.photo_filename:
            existing_photo_path = os.path.join(avatar_folder, user.photo_filename)
            if os.path.exists(existing_photo_path):
                os.remove(existing_photo_path)

        # Генерируем имя файла на основе порядкового номера
        avatar_count = len(os.listdir(avatar_folder))
        filename = str(avatar_count + 1) + '.jpg'

        # Сохраняем файл с новым именем
        file_path = os.path.join(avatar_folder, filename)
        file.save(file_path)

        # Обновляем имя файла фотографии пользователя в базе данных
        user.photo_filename = filename
        db.session.commit()

        flash('Файл успешно загружен')
        return redirect('/profile')

    flash('Неверный формат файла')
    return redirect('/profile')













with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
