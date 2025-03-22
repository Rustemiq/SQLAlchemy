from data import db_session
from data.users import User
from data.jobs import Job


db_sess = None
def create_db():
    db_sess = get_sess()
    user1 = User()
    user1.surname = 'Scott'
    user1.name = 'Ridley'
    user1.age = 21
    user1.position = 'captain'
    user1.speciality = 'research engineer'
    user1.address = 'module_1'
    user1.email = 'scott_chief@mars.org'
    user1.id = 1

    user2 = User()
    user2.surname = 'Ivanov'
    user2.name = 'Ivan'
    user2.age = 22
    user2.position = 'senior'
    user2.speciality = 'medic'
    user2.address = 'module_2'
    user2.email = 'ivanich@mars.org'
    user2.id = 2

    user3 = User()
    user3.surname = 'Petrov'
    user3.name = 'Petr'
    user3.age = 25
    user3.position = 'lieutenant'
    user3.speciality = 'architector'
    user3.address = 'module_1'
    user3.email = 'petrov@mars.org'
    user3.id = 3

    user4 = User()
    user4.surname = 'Fedorov'
    user4.name = 'Fedor'
    user4.age = 20
    user4.position = 'lieutenant'
    user4.speciality = 'engineer'
    user4.address = 'module_12'
    user4.email = 'fedooor@mars.org'
    user4.id = 4

    job1 = Job()
    job1.teamleader = 1
    job1.job = 'deployment of residential modules 1 and 2'
    job1.work_size = 15
    job1.collaborators = '2, 3'
    job1.is_finished = False
    job1.id = 1

    job2 = Job()
    job2.teamleader = 3
    job2.job = 'cleaning'
    job2.work_size = 5
    job2.collaborators = '1, 3'
    job2.is_finished = True
    job2.id = 2

    job3 = Job()
    job3.teamleader = 2
    job3.job = 'pretty hard job'
    job3.work_size = 30
    job3.collaborators = '2, 3'
    job3.is_finished = False
    job3.id = 3

    db_sess.add(user1)
    db_sess.add(user2)
    db_sess.add(user3)
    db_sess.add(user4)
    db_sess.add(job1)
    db_sess.add(job2)
    db_sess.add(job3)

    db_sess.commit()


def get_sess():
    db_name = 'mars_explorer.db'
    db_session.global_init(f"db/{db_name}")
    db_sess = db_session.create_session()
    return db_sess