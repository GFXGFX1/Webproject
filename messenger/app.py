from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit  # Импортируйте emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)


# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    content = db.Column(db.String(500))

# Создайте базу данных и таблицы
with app.app_context():
    db.create_all()


# Создание базы данных
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('chat'))

    return render_template('login.html')


@app.route('/chat')
def chat():
    if 'username' in session:
        messages = Message.query.all() 
        return render_template('chat.html', username=session['username'], messages=messages)
    return redirect(url_for('login'))

@socketio.on('send_message')
def handle_send_message(data):
    username = session.get('username', 'Аноним')  
    message = data['message']
    new_message = Message(username=username, content=message)
    db.session.add(new_message)
    db.session.commit()

    emit('receive_message', {'message': message, 'username': username}, broadcast=True)



if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
