import io
import json
import os

import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

resume_pdf_link = 'https://drive.google.com/open?id=0B2BrrDjIiyvmcWp5T194cy00UmM'


@app.route('/')
def index():
    age = int((datetime.date.today() - datetime.date(1995, 4, 22)).days / 365)
    return render_template('home.html', age=age)


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', resume_pdf_link=resume_pdf_link)


@app.route('/projects')
def projects():
    data = get_static_json("static/projects/projects.json")['projects']
    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('projects.html', projects=data, tag=tag)


@app.route('/experiences')
def experiences():
    return render_template('projects.html',
                           projects=get_static_json("static/experiences/experiences.json")['experiences'], tag=None)


@app.route('/projects/<title>')
def project(title):
    projects = get_static_json("static/projects/projects.json")['projects']
    experiences = get_static_json("static/experiences/experiences.json")['experiences']

    selected = next((p for p in projects if p['link'] == title), None)
    is_project = True
    if selected is None:
        selected = next((p for p in experiences if p['link'] == title), None)
        is_project = False
    if selected is None:
        return render_template('404.html'), 404

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "projects" if is_project else "experiences"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('project.html', project=selected)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))


if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
