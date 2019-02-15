from flask import Flask
import sys
import os
from flask import request
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
from greggo.feed_managers.base import FeedManager
app = Flask(__name__)

@app.route("/fanout")
def m_create_activity():
    json_body = request.get_json()
    if json_body:
        user_id = json_body["user_id"]
        activities = json_body["activities"]
        subscriptions = json_body["subscriptions"]

        FeedManager(user_id).create_activity(activities, subscriptions)
    return "DONE WITH"


if __name__ == "__main__":
    app.run()