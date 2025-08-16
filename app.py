from flask import Flask, render_template, request, jsonify
from google_play_scraper import search, app as playstore_app

flask_app = Flask(__name__)

def get_app_data(app_name):
    try:
        # Search with more specific parameters
        result = search(
            app_name,
            lang='en',
            country='us',
            n_hits=10,  # Get more results to find a better match
            detailed=True,  # Get more detailed search results
            full_detail=True,  # Get full details in the search
            price='all',  # Include both free and paid apps
            score_filtering=0  # Include all apps regardless of rating
        )
        
        if not result:
            return {"error": "No results found for the app."}
        
        # Find the best match using a scoring system
        best_match = None
        best_score = 0
        
        for app in result:
            score = 0
            title = app.get('title', '').lower()
            description = app.get('description', '').lower()
            query = app_name.lower()
            
            # Higher score for exact matches in title
            if query == title:
                score += 100
            # Partial matches in title
            elif query in title:
                score += 50 + (len(query) / len(title)) * 20
                
            # Matches in description (lower weight)
            if query in description:
                score += 10 + (len(query) / len(description)) * 5
                
            # Higher score for more installs (prioritize more popular apps)
            installs = str(app.get('installs', '0+')).replace('+', '').replace(',', '')
            if installs.isdigit():
                score += min(int(installs) / 10000, 50)  # Cap the install bonus at 50
                
            # Update best match if current app has higher score
            if score > best_score:
                best_score = score
                best_match = app
        
        # If no good match found, use the first result with a warning
        if not best_match and result:
            best_match = result[0]
            
        app_id = best_match['appId']
        
        # Get full app details
        app_details = playstore_app(
            app_id,
            lang='en',
            country='us',
            details=True  # Get more detailed information
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
