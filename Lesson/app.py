# The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for
# The second line says we'll use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
# The third line says that to use the scraping code, we will convert from Jupyter notebook to Python
import mars_scraping

# Setup Flask
app = Flask(__name__)
 
# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, 
    # URI: a uniform resource identifier similar to a URL
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, 
    # using port 27017, using a database named "mars_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create the route for the HTML page
@app.route("/")
# This function is what links our visual representation of our work, our web app, to the code that powers it
def index():
    # mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, 
        # which we will create when we convert our Jupyter scraping code to Python Script. 
        # We will also assign that path to the mars variable for use later
    mars = mongo.db.mars.find_one()
    # return render_template("index.html" tells Flask to return an HTML template using an index.html file. 
    # We'll create this file after we build the Flask routes
    # , mars=mars) tells Python to use the "mars" collection in MongoDB.
    return render_template("index.html", mars=mars)

# Create the route for the scraping 'button'
@app.route("/scrape")
# This function will scrape the updated data when we tell it to
# The next lines allow us to access the database, scrape new data using our scraping.py script, 
    # update the database, and return a message when successful
def scrape():
    # Assign a new variable that points to our Mongo database: mars = mongo.db.mars.
    mars = mongo.db.mars
    # created a new variable to hold the newly scraped data:
    # In this line, we're referencing the scrape_all function in the mars_scraping.py file 
        # exported from Jupyter Notebook
    mars_data = mars_scraping.scrape_all()
    # Now that we've gathered new data, we need to update the database using .update()
        # Syntax is as follows: .update(query_parameter, data, options)
            # {} inserts a blank json object
            # we will choose the scraped data we have placed in mars_data
            # upsert=True tells Mongo to create a new document if one doesn't already exist 
    mars.update({}, mars_data, upsert=True)
    # Finally, we will add a redirect after successfully scraping the data
    # This brings up back to the / route where we can see the updated data 
    return redirect('/', code=302)

# The final bit of code we need for Flask is to tell it to run
if __name__ == "__main__":
    app.run()