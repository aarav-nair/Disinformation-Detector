from bs4 import BeautifulSoup
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, redirect, request, send_from_directory
from flask_cors import CORS
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from model import trainModel, manual_testing
import requests

# My App
app = Flask(__name__)
CORS(app)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
 
class website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default= datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"URL {self.id}"
    
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('frontend/build', path)


@app.route('/')
def index():
    trainModel()
    return send_from_directory('react-frontend/build', 'index.html')

# @app.route("/", methods=["POST", "GET"])
# def index():
#     trainModel()
#     if request.method == "POST":
#         str = request.form['content']
#         new_url = website(content=str)
#         try:
#             db.session.add(new_url)
#             db.session.commit()
#             return redirect("/")
#         except Exception as e:
#             print(f"Error:{e}")
#             return f"Error:{e}"
        
#     else:
#         urls = website.query.order_by(website.created).all()
#         return render_template("index.html", urls=urls)

@app.route('/scrape', methods=['POST'])
def scrape():
    # data = request.get_json()
    # url = data.get('url')
    # print(f"Received URL: {url}")  # Debugging line
    # try:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         soup = BeautifulSoup(response.content, 'html.parser')
    #         content = soup.get_text(separator=' ', strip=True)
    #         content = manual_testing(url)
    #     else:
    #         content = "Error fetching the URL."
    # except Exception as e:
    #     content = f"An error occurred: {str(e)}"
    
    # return {'content': content}

    data = request.get_json()  # Get JSON data from React
    url = data.get('url')  # Extract the URL
    print(f"Received URL: {url}")  # Debugging line
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.get_text(separator=' ', strip=True)
            content = manual_testing(url)  # Your custom function
        else:
            content = "Error fetching the URL."
    except Exception as e:
        content = f"An error occurred: {str(e)}"

    # Return the scraped content as JSON
    return jsonify({'content': content})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
