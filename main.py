from flask import Flask, render_template
from scraper import scrape_dummy_data

app = Flask(__name__)


@app.route('/')
def index():
    context = {'values': scrape_dummy_data()}
    return render_template('index.html', context={'context': context})



if __name__ == '__main__':
    app.run(debug=True)