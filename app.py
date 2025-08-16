from flask import Flask, render_template, request, jsonify
from google_play_scraper import search as search_playstore, app as get_app_details

flask_app = Flask(__name__)

def get_app_data(app_name):
    try:
        # Simple search with minimal parameters
        results = search_playstore(
            app_name,
            lang='en',
            country='us',
            n_hits=3  # Limit to 3 results for better performance
        )
        
        if not results:
            return {"error": "No results found for the app."}
        
        # Get detailed information for each result
        detailed_results = []
        for result in results:
            try:
                app_id = result.get('appId')
                if not app_id:
                    continue
                    
                # Get detailed app information
                details = get_app_details(
                    app_id,
                    lang='en',
                    country='us'
                )
                
                detailed_results.append({
                    'title': details.get('title', 'N/A'),
                    'developer': details.get('developer', 'N/A'),
                    'installs': details.get('installs', 'Not available'),
                    'realInstalls': details.get('installs'),
                    'score': details.get('score', 'N/A'),
                    'ratings': details.get('ratings', 0)
                })
                
                # If we found a good match, return it immediately
                if app_name.lower() in details.get('title', '').lower():
                    return detailed_results[-1]
                    
            except Exception as e:
                print(f"Error getting details for {result.get('title')}: {str(e)}")
                continue
        
        # If no exact match found, return the first result
        if detailed_results:
            return detailed_results[0]
            
        return {"error": "Could not retrieve app details."}
        
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

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
