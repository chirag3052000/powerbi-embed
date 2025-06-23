from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

TENANT_ID = os.getenv("97731762-4437-411a-9438-1def5eb9188a")
CLIENT_ID = os.getenv("957043b2-d8d0-4038-b8a0-1df194e591c5")
CLIENT_SECRET = os.getenv("BSU8Q~P4g8Vxb-R17s~ekKHaAGSghzbmbo5ptdm4")
WORKSPACE_ID = os.getenv("fa0c62ce-0bd4-420d-a281-cc39696ebd3f")
REPORT_ID = os.getenv("5dcf93c4-4f60-43ef-a2ad-04ac9022c74a")

@app.route('/')
def index():
    return render_template("index.html", report_id=REPORT_ID, workspace_id=WORKSPACE_ID)

@app.route('/getEmbedToken')
def get_embed_token():
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'https://analysis.windows.net/powerbi/api/.default'
    }
    token_response = requests.post(token_url, data=data)
    access_token = token_response.json().get("access_token")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    embed_url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}/GenerateToken"
    embed_body = { "accessLevel": "View" }
    embed_response = requests.post(embed_url, headers=headers, json=embed_body)

    return jsonify(embed_response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
