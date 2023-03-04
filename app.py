
from requests import get, patch, post
from flask import Flask, request
from os import environ, path
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# app.config["DEBUG"] = True
PORT = int(environ.get("PORT"))
SECRET_KEY = environ.get("NOTION_TOKEN")

@app.route("/", methods = ["GET"])
def hello():
    return "hello world"

@app.route("/db/<db_id>", methods=["GET"])
def get_notion_db(db_id):
    response = post(f"https://api.notion.com/v1/databases/{db_id}/query",headers={
        "Notion-Version": "2022-06-28",
        "Authorization":f"Bearer {SECRET_KEY}",
        "Content-Type":"application/json"
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response.json()

@app.route("/page/<page_id>", methods=["GET"])
def get_notion_page(page_id):
    response = get(f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100",headers={
        "Notion-Version": "2022-06-28",
        "Authorization":f"Bearer {SECRET_KEY}",
        "Content-Type":"application/json"
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response.json()

@app.route("/feedback/<db_id>", methods=["POST"])
def post_feedback(db_id):
    content = request.json
    time_now = str(datetime.now())
    if "name" in content and "email" in content and "feedback" in content:
        response = post(f"https://api.notion.com/v1/pages",headers={
            "Notion-Version": "2022-06-28",
            "Authorization":f"Bearer {SECRET_KEY}",
            "Content-Type":"application/json"
        },
        json={
            "parent": { "database_id": db_id },
          "properties":{    
              "name": {
			"title": [
				{
					"text": {
						"content": content["name"]
					}
				}
			]
		},
		"email": {
			"rich_text": [
				{
					"text": {
						"content": content["email"]
					}
				}
			]
		},
        "feedback": {
			"rich_text": [
				{
					"text": {
						"content": content["feedback"]
					}
				}
			]
		}
        ,
        "date": {
			"rich_text": [
				{
					"text": {
						"content": time_now
					}
				}
			]
		}
        }
        }
        )
        
        return response.json()
    return "Check if name, email and feedback in json body"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
    # response_db = post(f"https://api.notion.com/v1/databases/{DB_ID}/query",headers={
    #     "Notion-Version": "2022-06-28",
    #     "Authorization":f"Bearer {SECRET_KEY}",
    #     "Content-Type":"app/json"
    # })
    # response = response_db.json()
    # for page_id in [page["id"] for page in response["results"]]:
    #     content = get(f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100",headers={
    #         "Notion-Version": "2022-06-28",
    #         "Authorization":f"Bearer {SECRET_KEY}",
    #         "Content-Type":"app/json"
    #     })
