from flask import Flask, render_template, request, jsonify
from google_play_scraper import search, app as get_app_details

flask_app = Flask(__name__)

def get_app_data(app_name):
    try:
        print(f"Searching for '{app_name}' on Google Play Store...")
        result = search(
            app_name,
            lang='en',
            country='us'
        )
        
        if not result:
            return {"error": "No results found for the app."}
            
        app_id = result[0]['appId']
        print(f"Found app with ID: {app_id}")
        
        app_details = get_app_details(
            app_id,
            lang='en',
            country='us'
        )
        
        installs = app_details.get('installs', 'Not available')
        real_installs = app_details.get('realInstalls')
        
        score = app_details.get('score', 'N/A')
        ratings = app_details.get('ratings', 0)
        if ratings is None:
            ratings = 0
            
        return {
            "title": app_details.get('title', 'N/A'),
            "developer": app_details.get('developer', 'N/A'),
            "installs": installs,
            "realInstalls": real_installs,
            "score": score,
            "ratings": ratings
        }
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}

@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/search', methods=['POST'])
def search_app():
    app_name = request.json.get('app_name', '')
    if not app_name:
        return jsonify({"error": "App name is required"}), 400
    return jsonify(get_app_data(app_name))

# For production with gunicorn
app = flask_app

if __name__ == '__main__':
    flask_app.run(debug=True)
