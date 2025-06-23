from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

TENANT_ID = os.getenv("TENANT_ID")         
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
REPORT_ID = os.getenv("REPORT_ID")

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

@app.route('/getEmbedToken')
def get_embed_token():
    try:
        token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': 'https://analysis.windows.net/powerbi/api/.default'
        }
        token_response = requests.post(token_url, data=data)
        access_token = token_response.json().get("access_token")

        if not access_token:
            return jsonify({"error": "Access token failed", "details": token_response.json()}), 500

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        embed_url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}/GenerateToken"
        embed_body = { "accessLevel": "View" }
        embed_response = requests.post(embed_url, headers=headers, json=embed_body)
        embed_data = embed_response.json()

        if "token" not in embed_data:
            return jsonify({"error": "Embed token failed", "details": embed_data}), 500

        return jsonify(embed_data)
    
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

