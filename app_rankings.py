import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


#################################################
# Database Setup
#################################################
engine = create_engine("postgresql://postgres:soemace123@localhost:5432/app_rankings")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save reference to the tables
Category = Base.classes.category
Application = Base.classes.application
Publisher = Base.classes.publisher
Ranking = Base.classes.ranking
Platform = Base.classes.platform

#################################################
# Flask Setup
#################################################
app = Flask(__name__, static_url_path='/static')


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():

    return render_template('index.html')

@app.route("/api")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/app_rankings_data"
    )

@app.route("/api/v1.0/app_rankings_data")
def app_rankings_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all app ranking data"""
    # Query all passengers
    sel = [Platform.platform, Publisher.publisher_name, Application.app_name, Ranking.date, Category.category, Ranking.rank]
    giant_query = session.query(*sel).filter(Ranking.app_id == Application.app_id).filter(Ranking.category_id == Category.category_id).filter(Ranking.platform_id == Platform.platform_id).filter(Application.publisher_id == Publisher.publisher_id).filter(Category.category_id == 2).order_by(Platform.platform).order_by(Publisher.publisher_name).order_by(Application.app_name).order_by(Ranking.date).order_by(Category.category).order_by(Ranking.rank).all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_apps = []
    current_pub_name = giant_query[0][1]
    current_app_name = giant_query[0][2]
    date_array = []
    app_array = []
    publisher_name_dict = {}
    app_name_dict = {}
    date_dict = {}
    all_apps = []

    for platform, publisher_name, app_name, date, category, rank  in giant_query:
    
        if app_name != current_app_name:
            app_name_dict["app_name"] = current_app_name
            app_name_dict["date"] = date_array
            date_array = []
            current_app_name = app_name
            app_array.append(app_name_dict)
            app_name_dict = {}
        
        if publisher_name != current_pub_name:
            publisher_name_dict["platform"] = platform
            publisher_name_dict["publisher_name"] = current_pub_name
            publisher_name_dict["app"] = app_array
            app_array = []
            current_pub_name = publisher_name
            all_apps.append(publisher_name_dict)
            publisher_name_dict = {}
        
        
        date_dict["date"] = date
        date_dict[f'{category}'] = rank
        date_array.append(date_dict)
        date_dict = {}

    return jsonify(all_apps)


if __name__ == '__main__':
    app.run(debug=True)
