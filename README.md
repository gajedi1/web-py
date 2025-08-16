# Google Play Store Scraper Web

A web application that allows you to search for apps on the Google Play Store and view their details including installs, ratings, and more.

## Features

- Search for any app on Google Play Store
- View detailed app information
- Clean and responsive web interface
- Real-time search results

## Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd playstore-scraper-web
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and go to `http://localhost:5000`

## Deployment

### Deploy to Render (Recommended)

1. Push your code to a GitHub repository
2. Sign up at [Render](https://render.com/) if you haven't already
3. Click "New" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - Name: `playstore-scraper` (or your preferred name)
   - Region: Choose the closest to you
   - Branch: `main` (or your default branch)
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. Click "Create Web Service"

Your app will be live at `https://your-app-name.onrender.com`

## Technologies Used

- Python 3
- Flask
- Google Play Scraper
- HTML/CSS/JavaScript
- Gunicorn (for production)

## License

This project is open source and available under the [MIT License](LICENSE).
