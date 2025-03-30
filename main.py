from data.create_db import create_db
from data import db_session
from data.users import User
from data.jobs import Job
from forms.job_addition import AdditionForm
from forms.user_registration import RegisterForm
from forms.user_login import LoginForm

from flask import Flask, render_template, redirect, request
from flask_login import login_user, LoginManager, current_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/works_log')
def works_log():
    db_sess = db_session.create_session()
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
        db_sess = db_session.create_session()
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
        db_sess = db_session.create_session()
        if not current_user.is_authenticated:
            return render_template('job_addition.html', title='Добавление работ',
                                   form=form,
                                   message="Авторизируйтесь чтобы добавить работу")
        if db_sess.query(Job).filter(Job.job == form.job.data).first():
            return render_template('job_addition.html', title='Добавление работ',
                                   form=form,
                                   message="Такая работа уже есть")
        creator = current_user.id
        job = Job(
            teamleader=form.teamleader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            creator=creator
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/works_log')
    return render_template('job_addition.html', title='Добавление работ', form=form)


@app.route('/select_job', methods=['GET', 'POST'])
def select_job():
    if not current_user.is_authenticated:
        available_jobs = []
    else:
        db_sess = db_session.create_session()
        available_jobs = db_sess.query(Job).filter(Job.creator == current_user.id | current_user.id == 1)
    return render_template('job_selection.html', title='Добавление работ', jobs=available_jobs)


@app.route('/change_job/<id>', methods=['GET', 'POST'])
def change_job(id):
    form = AdditionForm()
    db_sess = db_session.create_session()
    selected_job = db_sess.query(Job).filter(Job.id == id).first()
    if request.method == 'GET':
        form.teamleader.data = selected_job.teamleader
        form.job.data = selected_job.job
        form.work_size.data = selected_job.work_size
        form.collaborators.data = selected_job.collaborators
        form.is_finished.data = selected_job.is_finished

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return render_template('job_addition.html',
                                   title='Добавление работ',
                                   form=form,
                                   message="Авторизируйтесь чтобы изменить работу")
        if current_user.id != selected_job.creator and current_user.id != 1:
            return render_template('job_addition.html',
                                   title='Добавление работ',
                                   form=form,
                                   message="Недостаточно прав")
        db_sess = db_session.create_session()
        selected_job = db_sess.query(Job).filter(Job.id == id).first()
        selected_job.id = selected_job.id
        selected_job.teamleader=form.teamleader.data
        selected_job.job=form.job.data
        selected_job.job = form.job.data
        selected_job.work_size=form.work_size.data
        selected_job.collaborators=form.collaborators.data
        selected_job.is_finished=form.is_finished.data
        selected_job.creator=selected_job.creator
        db_sess.commit()
        return redirect('/works_log')
    return render_template('job_addition.html', title='Добавление работ',
                           form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
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
    db_session.global_init("db/mars_explorer.db")
    #create_db()
    app.run(port=8080, host='127.0.0.1')