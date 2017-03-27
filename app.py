# -*- coding: utf-8 -*-
import json
import os
from chalice import Chalice
import requests

app = Chalice(app_name='esa_then_qiita')
app.debug = True
API_URL = u"http://qiita.com/api/v2/"

API_KEY = os.environ["QIITA_API_KEY"]
QIITA_USER = os.environ["QIITA_USER"]
SLACK_HOOK_URL = os.environ["SLACK_HOOK_URL"]

@app.route('/qiita', methods=['POST'])
def index():
    # parse request
    request = app.current_request.json_body
    raw_title = request["post"]["name"].split(u"/")[-1]
    title_and_tags = [ i.strip() for i in raw_title.split("#") ]

    # find qiita tag
    if u"qiita" not in title_and_tags:
        return u"nothing to do (this is not the post for qiita)"

    # check articles duplication
    past_items = requests.get(url=API_URL + 'items?page=1&per_page=20&query=user%3A' + QIITA_USER)
    past_titles = [ item["title"] for item in past_items.json() ]
    while "next" in past_items.links:
        past_items = requests.get(past_items.links["next"]["url"])
        past_titles.extend([ item["title"] for item in past_items.json() ])
    if title_and_tags[0] in past_titles:
        return u"nothing to do (same title post already exists)"

    # set up qiita request
    qiita_input_dict = {
        "title": title_and_tags[0],
        "body": request["post"]["body_md"],
        "gist": False,
        "private": False,
        "tweet": False,
        "tags": [ {"name": tag} for tag in title_and_tags[1:] if tag.find(u"qiita") == -1 ]
    }
    headers = {
        "Authorization": u"Bearer " + API_KEY,
        "Content-Type": u"application/json",
        "Accept": u"application/json"
    }

    # post qiita
    r = requests.post(url=API_URL + "items", data=json.dumps(qiita_input_dict), headers=headers)

    # post result to slack
    slack_input_dict = {
        "text": u"esa.io -> qiita done.\n{}".format(r.json()["url"]),
        "channel": u"develops"
    }
    print r.status_code
    if r.status_code == 201 and SLACK_HOOK_URL != "":
        re = requests.post(url=SLACK_HOOK_URL, data=json.dumps(slack_input_dict))
    return r.text
