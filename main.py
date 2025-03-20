from data import db_session
from data.users import User


def main():
    db_session.global_init("db/mars_explorer.db")
    user1 = User()
    user1.surname = 'Scott'
    user1.name = 'Ridley'
    user1.age = 21
    user1.position = 'captain'
    user1.speciality = 'research engineer'
    user1.address = 'module_1'
    user1.email = 'scott_chief@mars.org'
    user2 = User()
    user2.surname = 'Ivanov'
    user2.name = 'Ivan'
    user2.age = 22
    user2.position = 'senior'
    user2.speciality = 'medic'
    user2.address = 'module_2'
    user2.email = 'ivanich@mars.org'

    user3 = User()
    user3.surname = 'Petrov'
    user3.name = 'Petr'
    user3.age = 25
    user3.position = 'lieutenant'
    user3.speciality = 'architector'
    user3.address = 'module_5'
    user3.email = 'petrov@mars.org'

    user4 = User()
    user4.surname = 'Fedorov'
    user4.name = 'Fedor'
    user4.age = 20
    user4.position = 'lieutenant'
    user4.speciality = 'engineer'
    user4.address = 'module_12'
    user4.email = 'fedooor@mars.org'


if __name__ == '__main__':
    main()