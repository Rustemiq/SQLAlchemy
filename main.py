from data.create_db import create_db, get_sess
from data.jobs import Job

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
@app.route('/works_log')
def works_log():
    db_sess = get_sess()
    jobs = db_sess.query(Job).all()
    return render_template('works_log.html', jobs=jobs)


if __name__ == '__main__':
    #create_db()
    app.run(port=8080, host='127.0.0.1')