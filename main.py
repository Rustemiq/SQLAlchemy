from data import db_session
from data.category import Category
from data.departments import Department
from data.users import User
from data.jobs import Job
from forms.depart_addition import DepartAdditionForm
from forms.job_addition import JobAdditionForm
from forms.user_registration import RegisterForm
from forms.user_login import LoginForm
from data.create_db import create_db
import data.jobs_api as jobs_api
import data.users_api as users_api

from flask import Flask, render_template, redirect, request, make_response, jsonify
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
    if current_user.is_authenticated:
        editable_jobs = db_sess.query(Job).filter((Job.creator == current_user.id) | (current_user.id == 1))
    else:
        editable_jobs = []
    return render_template('works_log.html', jobs=jobs, current_user=current_user, editable_jobs=editable_jobs)


@app.route('/')
@app.route('/departs_log')
def departs_log():
    db_sess = db_session.create_session()
    departs = db_sess.query(Department).all()
    if current_user.is_authenticated:
        editable_departs = db_sess.query(Department).filter((Department.creator == current_user.id) | (current_user.id == 1))
    else:
        editable_departs= []
    return render_template('departs_log.html', departs=departs, current_user=current_user, editable_departs=editable_departs)



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
    form = JobAdditionForm()
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
        for category in form.categories.data.split(','):
            job.categories.append(db_sess.query(Category).filter(Category.id == category).first())

        db_sess.add(job)
        db_sess.commit()
        return redirect('/works_log')
    return render_template('job_addition.html', title='Добавление работ', form=form)


@app.route('/add_depart', methods=['GET', 'POST'])
def add_depart():
    form = DepartAdditionForm()
    if not current_user.is_authenticated:
        return render_template('depart_addition.html', title='Добавление департаментов',
                               form=form,
                               message="Авторизируйтесь чтобы добавить департамент")
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        creator = current_user.id
        depart = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data,
            creator=creator
        )
        db_sess.add(depart)
        db_sess.commit()
        return redirect('/departs_log')
    return render_template('depart_addition.html', title='Добавление департаментов', form=form)


@app.route('/change_job/<id>', methods=['GET', 'POST'])
def change_job(id):
    form = JobAdditionForm()
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
        selected_job.teamleader = form.teamleader.data
        selected_job.job = form.job.data
        selected_job.work_size = form.work_size.data
        selected_job.collaborators = form.collaborators.data
        selected_job.is_finished = form.is_finished.data
        selected_job.creator = selected_job.creator
        db_sess.commit()
        return redirect('/works_log')
    return render_template('job_addition.html', title='Добавление работ',
                           form=form)


@app.route('/change_depart/<id>', methods=['GET', 'POST'])
def change_depart(id):
    form = DepartAdditionForm()
    db_sess = db_session.create_session()
    selected_depart = db_sess.query(Department).filter(Department.id == id).first()
    if request.method == 'GET':
        form.title.data = selected_depart.title
        form.chief.data = selected_depart.chief
        form.members.data = selected_depart.members
        form.email.data = selected_depart.email

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return render_template('depart_addition.html',
                                   title='Добавление работ',
                                   form=form,
                                   message="Авторизируйтесь чтобы изменить департамент")
        if current_user.id != selected_depart.creator and current_user.id != 1:
            return render_template('depart_addition.html',
                                   title='Добавление работ',
                                   form=form,
                                   message="Недостаточно прав")
        db_sess = db_session.create_session()
        selected_depart = db_sess.query(Department).filter(Department.id == id).first()
        selected_depart.title = form.title.data
        selected_depart.chief = form.chief.data
        selected_depart.members = form.members.data
        selected_depart.email = form.email.data
        db_sess.commit()
        return redirect('/departs_log')
    return render_template('depart_addition.html', title='Добавление департаментов',
                           form=form)


@app.route('/delete_job/<id>')
def delete_job(id):
    db_sess = db_session.create_session()
    db_sess.query(Job).filter(Job.id == id).delete()
    db_sess.commit()
    return redirect('/')


@app.route('/delete_depart/<id>')
def delete_depart(id):
    db_sess = db_session.create_session()
    db_sess.query(Department).filter(Department.id == id).delete()
    db_sess.commit()
    return redirect('/departs_log')


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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    #create_db()
    db_session.global_init("db/mars_explorer.db")

    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == 1).first()

    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)

    app.run(port=8080, host='127.0.0.1')