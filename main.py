from data.create_db import create_db, get_sess
from data import db_session
from data.users import User
from data.jobs import Job
from forms.job_addition import AdditionForm
from forms.user_registration import RegisterForm
from forms.user_login import LoginForm

from flask import Flask, render_template, redirect
from flask_login import login_user, LoginManager, current_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = get_sess()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/works_log')
def works_log():
    db_sess = get_sess()
    jobs = db_sess.query(Job).all()
    return render_template('works_log.html', jobs=jobs, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = get_sess()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AdditionForm()
    if form.validate_on_submit():
        db_sess = get_sess()
        if not current_user.is_authenticated:
            return render_template('job_addition.html', title='Добавление работ',
                                   form=form,
                                   message="Авторизируйтесь чтобы добавить работу")
        if db_sess.query(Job).filter(Job.job == form.job.data).first():
            return render_template('job_addition.html', title='Добавление работ',
                                   form=form,
                                   message="Такая работа уже есть")
        job = Job(
            teamleader=form.teamleader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/works_log')
    return render_template('job_addition.html', title='Добавление работ', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = get_sess()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/works_log")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    #create_db()
    app.run(port=8080, host='127.0.0.1')