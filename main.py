# To run: 
# flask --app main --debug run

import datetime
import json
from flask import Flask, redirect, render_template, request, send_from_directory
import requests
from pprint import pprint

INDEX_CONFIG_FILE = "./config/index.json"
VOTE_CONFIG_FILE = "./config/vote.json"
IDEAS_CONFIG_FILE = "./config/ideas.json"
NOT_FOUND_PAGE_CONDIG_FILE = "./config/404.json"

APP = Flask(__name__)

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=6000, debug=True)
    APP.debug = True

def getIndexConfig():
    with open(INDEX_CONFIG_FILE, "r") as f:
        return json.load(f)

def getPageNotFoungConfig():
    with open(NOT_FOUND_PAGE_CONDIG_FILE, "r") as f:
        return json.load(f)

def getVoteConfig():
    with open(VOTE_CONFIG_FILE, "r") as f:
        return json.load(f)

def getIdeasConfig():
    with open(IDEAS_CONFIG_FILE, "r") as f:
        return json.load(f)

def saveIdeasConfig(cfg):
    with open(IDEAS_CONFIG_FILE, "w") as f:
        f.write(json.dumps(cfg, indent=4))

@APP.route('/', methods=['GET'])
def index():
    return render_template('index.html', config = getIndexConfig())

@APP.route('/vote', methods=['GET', 'POST'])
def vote():
    ideas = getIdeasConfig()

    if request.method == 'POST':
        form = request.form.to_dict()

        id = form['idea_id']
        if not id:
            return redirect('/vote')

        is_updated = False
        for idea in ideas:
            if idea['id'] == id:
                if 'upvote' in form:
                    idea['reit'] += 1
                    is_updated = True
                elif 'downvote' in form:
                    idea['reit'] -= 1
                    is_updated = True

        if is_updated:
            ideas = sorted(ideas, key=lambda k: k['reit'], reverse=True)
            saveIdeasConfig(ideas)

        return  redirect('/vote')

    return render_template('vote.html', config=getVoteConfig(), ideas=ideas)

@APP.route('/voteAdd', methods=['GET', 'POST'])
def voteAdd():
    if request.method == 'POST':
        form = request.form.to_dict()
        pprint(form)

        ideas = getIdeasConfig()
        ideas.append({
            'id': str(len(ideas) +  1),
            'name': form['idea'],
            'description': form['description'],
            'contact': form['contact'],
            'reit': 0,
        })
        saveIdeasConfig(ideas)

        return redirect('/vote')

    return render_template('vote_add.html', config=getVoteConfig())

@APP.route('/style/<path:path>')
def send_style(path):
    return send_from_directory('style', path)

@APP.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)

@APP.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', config = getPageNotFoungConfig()), 404
