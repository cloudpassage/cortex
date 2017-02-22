from flask import Flask
from flask import render_template
from octoutils.utility import Utility as util
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('mainpage.html')

@app.route('/job-list')
def reports_page():
    return render_template('job-list.html', tasks=util.get_celery_tasks())
