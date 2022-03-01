import flask
from flask import request, jsonify, render_template

from . import db_session
from .jobs import Jobs
from .news import News

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {'jobs': [
            item.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                               'collaborators', 'start_date', 'is_finished')) for item in jobs]})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {'jobs': job.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                   'collaborators', 'start_date', 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size',
                  'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    exist_id = db_sess.query(Jobs).get(request.json['id'])

    if exist_id is not None:
        return jsonify({'error': 'Id already exists'})

    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )

    db_sess.add(job)
    db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})
