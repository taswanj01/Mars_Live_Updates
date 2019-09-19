from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_app"
mongo = PyMongo(app)

# Define home page route
@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

# Define route to scrape for new data
@app.route("/mars_scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_scrape_data = mars_scrape.mars_scrape()
    mars_data.update({}, mars_scrape_data, upsert=True)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)
