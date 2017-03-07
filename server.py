from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Country, Country_Search
from sqlalchemy import desc, func
import json 
import flickrapi
import helper

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Raises error if undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    countries = Country.query.order_by('country_name').all()
    return render_template("register_form.html", countries=countries)


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]
    home_country = request.form["country_code"]

    user = User.query.filter_by(email=email).first()

    if not user:
        new_user = User(fname=fname, lname=lname, email=email, password=password, age=age, zipcode=zipcode, home_country=home_country)
        db.session.add(new_user)
        db.session.commit()
        flash("User %s added." % email)
        return redirect("/")
    else:
        flash("This email is already registered. Please log in!")
        return redirect("/login")
    

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


@app.route("/button", methods=['GET'])
def country_search_button():
    """Chosen button for search"""

    nations = Country.query.order_by('country_name').all()
    return render_template("search_button.html", nations=nations)


@app.route("/cost_of_living_map")
def display_map():
    """Render cost of living map"""

    return render_template("cost_of_living_map.html")


@app.route("/top_ten_list")
def top_ten_list():
    """List top 10 least expensive countries"""
    pass


@app.route("/map_of_world", methods=["GET"])
def choose_countries():
    """Choose 3-5 countries to compare based on map & top 10 list"""

    nations = Country.query.order_by('country_name').all()
    return render_template("pick_countries.html", nations=nations)


@app.route("/display_chosen_countries", methods=["GET"])
def display_chosen_countries():
    """Display the Flick pictures, cost of living factors, and Kiva links for 
    the countries the user chose via the Chosen button. """

    user_id = session.get("user_id")
    
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()

    nations = request.args.getlist('countries')
    country_info = []
    urls = []

    for nation in nations: 
        url = "https://www.kiva.org/lend?country="
        country = Country.query.filter_by(country_name=nation).first()
        country_name = country.country_name
        country_name = str(country_name)
        country_pic = helper.flickr_pics(country_name)
        urls.append(country_pic)

        if country: 
            country_with_urls = {}
            country_with_urls[country] = url + country.country_code
            country_info.append(country_with_urls)

    return render_template("country_display.html", country_info=country_info, user=user, urls=urls)


@app.route("/col_index.json", methods=["GET"])
def getCpiIndex():

    """ Provide Google charts with values to display on world map (Ajax call result)"""

    return jsonify(helper.process_country_factor("col_index"))


@app.route("/bread_price.json", methods=["GET"])
def getBreadPrice():
    
    """ Provide Google charts with values to display on world map (Ajax call result)"""

    return jsonify(helper.process_country_factor("bread_price"))


@app.route("/meal_price.json", methods=["GET"])
def getMealPrice():
  
    """ Provide Google charts with values to display on world map (Ajax call result)"""
    
    return jsonify(helper.process_country_factor("meal_price"))


@app.route("/apt_price.json", methods=["GET"])
def getAptPrice():
  
    """ Provide Google charts with values to display on world map (Ajax call result)"""

    return jsonify(helper.process_country_factor("apt_price"))


@app.route("/health_care_index.json", methods=["GET"])
def getHealthCarePrice():

    """ Provide Google charts with values to display on world map (Ajax call result)"""

    return jsonify(helper.process_country_factor("health_care_index"))


@app.route("/crime_index.json", methods=["GET"])
def getCrimeIndex():

    return jsonify(helper.process_country_factor("crime_index"))

@app.route("/pollution_index.json", methods=["GET"])
def getPollutionIndex():

    """ Provide Google charts with values to display on world map (Ajax call result)"""

    return jsonify(helper.process_country_factor("pollution_index"))


@app.route("/traffic_index.json", methods=["GET"])
def getTrafficIndex():

    """ Provide Google charts with values to display on world map (Ajax call result)"""

    return jsonify(helper.process_country_factor("traffic_index"))


@app.route("/groceries_index.json", methods=["GET"])
def getGroceriesIndex():

    """ Provide Google charts with values to display on world map (Ajax call result)"""

    return jsonify(helper.process_country_factor("groceries_index"))


@app.route("/rent_index.json", methods=["GET"])
def getRentIndex():

    """ Provide Google charts with values to display on world map (Ajax call result)"""

    return jsonify(helper.process_country_factor("rent_index"))


@app.route("/property_price_to_income_ratio.json", methods=["GET"])
def getPropertyPricetoIncome():

    """ Provide Google charts with values to display on world map (Ajax call result)"""

    return jsonify(helper.process_country_factor("property_price_to_income_ratio"))


@app.route("/multiFormPick.json", methods=["GET"])
def multiFormPick():

    col_index = request.args.get('colindex')
    bread_price = request.args.get('breadprice')
    meal_price = request.args.get('mealprice')
    apt_price = request.args.get('apt_price')
    groceries_index = request.args.get('groceries_index')
    rent_index = request.args.get('rent_index')
    property_price_to_income_ratio = request.args.get('property_price_to_income_ratio')
    crime_index = request.args.get('crime_index')
    health_care_index = request.args.get('health_care_index')
    pollution_index = request.args.get('pollution_index')
    traffic_index = request.args.get('traffic_index')

    country_list = []

    q = db.session.query(Country.country_name, Country.col_index)

    if col_index: 
        q = q.filter(Country.col_index < col_index)

    if bread_price:
        q = q.filter(Country.bread_price < bread_price)

    if meal_price:
        q = q.filter(Country.meal_price < meal_price)

    if apt_price:
        q = q.filter(Country.apt_price < apt_price)

    if groceries_index:
        q = q.filter(Country.groceries_index < groceries_index)

    if rent_index:
        q = q.filter(Country.rent_index < rent_index)

    if property_price_to_income_ratio:
        q = q.filter(Country.property_price_to_income_ratio < property_price_to_income_ratio)

    if health_care_index:
        q = q.filter(Country.health_care_index < health_care_index)

    if crime_index:
        q = q.filter(Country.crime_index < crime_index)

    if pollution_index:
        q = q.filter(Country.pollution_index < pollution_index)

    if traffic_index:
        q = q.filter(Country.traffic_index < traffic_index)

    q = q.all()

    for country,factor in q:
        country_list.append([country, factor])

    results = {'items': country_list}

    return jsonify(results)
    # return jsonify(process_multiple_country_factors())


@app.route('/country_picks.json')
def country_picks_data():
    """Return data about Country picks."""

    # print "ENTERING COUNTRY PICKS"

    # request.args returns a multidict with countryList[] as keys

    user_id = session.get("user_id")
    
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()

    country_list = request.args.getlist("countryList[]")
    
    countries = [user.country.country_name]
    info = [user.country.meal_price]

    for nation in country_list:
        country = Country.query.filter_by(country_code=nation).first()
        countries.append(country.country_name)
        info.append(country.meal_price)

    data = {
                "labels": countries,
                "datasets": [
                    {
                        "data": info,
                        
                        "backgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56",
                            "#FFFFEE",
                            "#98fb98" 

                        ],

                        "hoverBackgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56",
                            "#FFFFEE",
                            "#98fb98"
                        ]
                    }]
            }
 
    return jsonify(data)

@app.route('/explain_indices')
def explain_indices():

    return render_template("/explain_indices.html")


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
    
    app.run(port=5000, host='0.0.0.0')

