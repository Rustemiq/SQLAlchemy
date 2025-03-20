from data import db_session
from data.users import User


def main():
    db_session.global_init("db/astronauts.db")


if __name__ == '__main__':
    main()