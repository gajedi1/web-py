from flask import Flask, render_template, request, jsonify
from google_play_scraper import search, app

app = Flask(__name__)

def get_app_data(app_name):
    try:
        result = search(
            app_name,
            lang='en',
            country='us'
        )
        
        if not result:
            return {"error": "No results found for the app."}
            
        app_id = result[0]['appId']
        app_details = app(
            app_id,
            lang='en',
            country='us'
        )
        
        return {
            "title": app_details.get('title', 'N/A'),
            "developer": app_details.get('developer', 'N/A'),
            "installs": app_details.get('installs', 'Not available'),
            "realInstalls": app_details.get('realInstalls'),
            "score": app_details.get('score', 'N/A'),
            "ratings": app_details.get('ratings', 0) or 0
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_app():
    app_name = request.json.get('app_name', '')
    if not app_name:
        return jsonify({"error": "App name is required"}), 400
    return jsonify(get_app_data(app_name))

if __name__ == '__main__':
    app.run(debug=True)
