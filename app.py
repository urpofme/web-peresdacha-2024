from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице, пожалуйста, войдите в систему.'

# Данные пользователя (обычно в базе данных, здесь для примера)
users = {
    'user': generate_password_hash('qwerty')
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

# Страница главная
@app.route('/')
def home():
    return render_template('home.html', user=current_user)

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form
        
        if username in users and check_password_hash(users[username], password):
            user = User(username)
            login_user(user, remember=remember)
            flash('Вы успешно вошли!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Неверный логин или пароль.', 'danger')
    
    return render_template('login.html')

# Страница выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('home'))

# Секретная страница
@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

# Счётчик посещений
@app.route('/counter')
def counter():
    session['visits'] = session.get('visits', 0) + 1
    return f'Количество посещений этой страницы: {session["visits"]}'

if __name__ == '__main__':
    app.run(debug=True)
