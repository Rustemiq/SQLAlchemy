import flask
import datetime

from . import db_session
from .users import User
from flask import jsonify, make_response, request


blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(
                    only=(
                        'id',
                        'login',
                        'surname',
                        'name',
                        'age',
                        'position',
                        'speciality',
                        'address',
                        'modified_date',
                        'city_from'
                    )
                )
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'users':
            [
                user.to_dict(
                    only=(
                        'id',
                        'login',
                        'surname',
                        'name',
                        'age',
                        'position',
                        'speciality',
                        'address',
                        'modified_date',
                        'city_from'
                        )
                    )
            ]
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    req_json = request.json
    if not req_json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in req_json for key in
                 ['login', 'surname', 'name', 'age', 'position',
                  'speciality', 'address']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = User(
        login=req_json['login'],
        surname=req_json['surname'],
        name=req_json['name'],
        age=req_json['age'],
        position=req_json['position'],
        speciality=req_json['speciality'],
        address=req_json['address'],
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def put_job(user_id):
    req_json = request.json
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    user.login = req_json.get('login', user.login)
    user.surname = req_json.get('surname', user.surname)
    user.name = req_json.get('name', user.name)
    user.age = req_json.get('age', user.age)
    user.position = req_json.get('position', user.position)
    user.speciality = req_json.get('speciality', user.speciality)
    user.address = req_json.get('address', user.address)
    user.modified_date = datetime.datetime.now()

    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})