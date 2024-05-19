from flask import Flask, render_template
from scraper import scrape_dummy_data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', context=scrape_dummy_data())



if __name__ == '__main__':
    app.run(debug=True)
