from data import db_session
from data.users import User
from data.jobs import Job


def main():
    db_name = input('db name ->')
    db_session.global_init(f"db/{db_name}")
    user1 = User()
    user1.surname = 'Scott'
    user1.name = 'Ridley'
    user1.age = 21
    user1.position = 'captain'
    user1.speciality = 'research engineer'
    user1.address = 'module_1'
    user1.email = 'scott_chief@mars.org'
    user1.id = 0

    user2 = User()
    user2.surname = 'Ivanov'
    user2.name = 'Ivan'
    user2.age = 22
    user2.position = 'senior'
    user2.speciality = 'medic'
    user2.address = 'module_2'
    user2.email = 'ivanich@mars.org'
    user2.id = 1

    user3 = User()
    user3.surname = 'Petrov'
    user3.name = 'Petr'
    user3.age = 25
    user3.position = 'lieutenant'
    user3.speciality = 'architector'
    user3.address = 'module_1'
    user3.email = 'petrov@mars.org'
    user3.id = 2

    user4 = User()
    user4.surname = 'Fedorov'
    user4.name = 'Fedor'
    user4.age = 20
    user4.position = 'lieutenant'
    user4.speciality = 'engineer'
    user4.address = 'module_12'
    user4.email = 'fedooor@mars.org'
    user4.id = 3

    job1 = Job()
    job1.teamleader = 1
    job1.job = 'deployment of residential modules 1 and 2'
    job1.work_size = 15
    job1.collaborators = '2, 3'
    job1.is_finished = False
    job1.id = 0

    db_sess = db_session.create_session()
    db_sess.add(user1)
    db_sess.add(user2)
    db_sess.add(user3)
    db_sess.add(user4)
    db_sess.add(job1)

    db_sess.commit()

    for user in db_sess.query(User).filter(User.address == 'module_1'):
        print(user)


if __name__ == '__main__':
    main()