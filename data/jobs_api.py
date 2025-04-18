import flask

from . import db_session
from .jobs import Job
from flask import jsonify, make_response, request
from data.category import Category


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(
                    only=(
                        'id',
                        'teamleader',
                        'user.name',
                        'user.surname',
                        'job',
                        'work_size',
                        'collaborators',
                        'start_date',
                        'end_date',
                        'is_finished',
                        'creator',
                        'categories'
                    )
                )
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == job_id).first()
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs':
                job.to_dict(
                    only=(
                        'id',
                        'teamleader',
                        'user.name',
                        'user.surname',
                        'job',
                        'work_size',
                        'collaborators',
                        'start_date',
                        'end_date',
                        'is_finished',
                        'creator',
                        'categories'
                    )
                )
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    req_json = request.json
    if not req_json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    if (
            type(req_json['teamleader']) is not int or \
            type(req_json['job']) is not str or \
            type(req_json['work_size']) is not int or \
            type(req_json['collaborators']) is not str or \
            type(req_json['is_finished']) is not bool or \
            type(req_json['categories']) is not str or \
            type(req_json['creator']) is not int
    ):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    elif not all(key in req_json for key in
                 ['teamleader', 'job', 'work_size', 'collaborators', 'is_finished', 'categories', 'creator']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    job = Job(
        teamleader=req_json['teamleader'],
        job=req_json['job'],
        work_size=req_json['work_size'],
        collaborators=req_json['collaborators'],
        is_finished=req_json['is_finished'],
        creator=req_json['creator']
    )
    for category in request.json['categories'].split(','):
        category_item = db_sess.query(Category).filter(Category.id == category).first()
        if not category_item:
            return make_response(jsonify({'error': 'Not found'}), 404)
        job.categories.append(category_item)
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def put_job(job_id):
    req_json = request.json
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == job_id).first()
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    job.teamleader = req_json.get('teamleader', job.teamleader)
    job.job = req_json.get('job', job.job)
    job.work_size = req_json.get('work_size', job.work_size)
    job.collaborators = req_json.get('collaborators', job.collaborators)
    job.is_finished = req_json.get('is_finished', job.is_finished)
    job.creator = req_json.get('creator', job.creator)
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})