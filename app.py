from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

#start up flask
app = Flask(__name__)

# instantiating mongo
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_data')
db = mongo.db

@app.route('/')
def index():
    mars_info = db.mars.find_one()
    return render_template('index.html', mars_data=mars_info)

@app.route('/scrape')
def scraper():
    mars = scrape()
    db.mars_data.update({}, mars, upsert=True)

    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)