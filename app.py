from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.get_text(separator=' ', strip=True) 
            content = ' '.join(content.split()[:500])
        else:
            content = "Error fetching the URL."
    except Exception as e:
        content = f"An error occurred: {str(e)}"
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
