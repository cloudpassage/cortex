import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import Response
from halocelery import tasks
from octoutils.utility import Utility as util
from octoutils.halo import Halo as halo


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route('/')
def home_page():
    return render_template('mainpage.html')

@app.route('/job-list')
def job_list():
    return render_template('job-list.html', tasks=util.get_celery_tasks())

@app.route('/reports', methods=['GET'])
def reports_page():
    return render_template('reports.html', reports=get_reports_status(session["reports"]),
                                           server_list=halo.list_all_servers(),
                                           group_list=halo.list_all_groups())

@app.route('/reports', methods=['POST'])
def initiate_report():
    target_id = request.form['target_id']
    report_type = request.form['report_type']
    session["reports"].append(start_report_job(report_type, target_id))
    return render_template()

@app.route('/render', methods=['GET'])
def render_report():
    job = get_job_by_id(request.args["job_id"])
    mimeref = {"png": "image/png"}
    if job:
        if job.ready():
            return Response(job["task_obj"].get(), mimeref["SOMETHING_HERE"])
        content = ""
    return Response(content)

def get_job_by_id(job_id):
    for job in session["reports"]:
        if job.id == job_id:
            return job
    return None

def get_reports_status(reports):
    retval = []
    for report in reports:
        rep_ret = report.copy()
        if report["task_obj"].ready():
            rep_ret["ready"] = True
        else:
            rep_ret["ready"] = False
        retval.append(rep_ret)
    return retval

def start_report_job(report_type, target_id):
    retval = {"report_type": "", "format": "txt"}
    if report_type == "compliance_graph":
        retval["task_obj"] = tasks.report_server_scan_graph.delay(target_id)
        retval["format"] = "png"
        retval["report_type"] = report_type
    return retval
