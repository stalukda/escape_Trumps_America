from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Country, Country_Search
from sqlalchemy import desc, func
import json 
import flickrapi

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

    #query for country + code 
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
        # new_country_user = Country_Search(new_user)
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

    countries = Country.query.order_by('country_name').all()
    nations = []

    for country in countries:
        if country.bread_price != 'None': 
            nations.append(country)
        else: 
            pass 

    return render_template("cost_of_living_map.html", nations=nations)


@app.route("/top_ten_list")
def top_ten_list():
    """List top 10 least expensive countries"""
    pass


@app.route("/map_of_world", methods=["GET"])
def choose_countries():
    """Choose 3-5 countries to compare based on map & top 10 list"""

    nations = Country.query.order_by('country_name').all()
    return render_template("pick_countries.html", nations=nations)


@app.route("/compare_countries", methods=["GET"])
def compare_countries():
    """Compare the 3-5 chosen countries"""

    #gather a list of country URLs
    #send to front end 
    #iterate through and create images 

    user_id = session.get("user_id")
    
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()

    nations = request.args.getlist('countries')
    country_info = []
    urls = []

    for nation in nations: 
        url = "https://www.kiva.org/lend?country="
        #check each nation picked against the db 
        country = Country.query.filter_by(country_name=nation).first()
        country_name = country.country_name
        country_name = str(country_name)
        country_pic = flickr_pics(country_name)
        urls.append(country_pic)

        if country: 
            country_with_urls = {}
            country_with_urls[country] = url + country.country_code
            country_info.append(country_with_urls)

    print "*" * 20
    print country_info 
    print urls
    return render_template("country_display.html", country_info=country_info, user=user, urls=urls)

def flickr_pics(country_name):

    api_key = u'9489272c64643fc71165347fccfebbc0'
    api_secret = u'81789d543c6d0977'
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    country = "amazing view" + " " + country_name 
    photo = flickr.photos.search(per_page='1', format='json', text=country)
    photo_info = json.loads(photo)

    farm_id = photo_info['photos']['photo'][0]['farm']
    server_id = photo_info['photos']['photo'][0]['server']
    photo_id = photo_info['photos']['photo'][0]['id']
    secret = photo_info['photos']['photo'][0]['secret']

    user_id = photo_info['photos']['photo'][0]['owner']

    photo_source_template = "https://flickr.com/photos/{}/{}/"
    photo_source_url = photo_source_template.format(user_id, photo_id)

    static_photo_source_template = "https://farm{}.staticflickr.com/{}/{}_{}.jpg"
    static_photo_source_url = static_photo_source_template.format(farm_id, server_id, photo_id, secret)
    return static_photo_source_url

@app.route("/col_index.json", methods=["GET"])
def getCpiIndex():

    nations = Country.query.order_by('country_name').all()
    min_val_country = Country.query.order_by('col_index').first()
    min_val = min_val_country.col_index
    max_val = 0

    country_list = []

    for nation in nations: 
        if nation.col_index:
            country_list.append([nation.country_name, nation.col_index])
        if nation.col_index > max_val: 
            max_val = nation.col_index

    results = {'items': country_list, 'min_val': min_val, 'max_val': max_val}

    return jsonify(results)


@app.route("/bread_price.json", methods=["GET"])
def getBreadPrice():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.bread_price:
            country_list.append([nation.country_name, nation.bread_price])

    results = {'items': country_list}

    print "*" * 20 
    print results

    return jsonify(results)



@app.route("/meal_price.json", methods=["GET"])
def getMealPrice():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.meal_price:
            country_list.append([nation.country_name, nation.meal_price])

    results = {'items': country_list}

    return jsonify(results)


@app.route("/apt_price.json", methods=["GET"])
def getAptPrice():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.apt_price:
            country_list.append([nation.country_name, nation.apt_price])

    results = {'items': country_list}

    return jsonify(results)


@app.route("/health_care_index.json", methods=["GET"])
def getHealthCarePrice():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.health_care_index:
            country_list.append([nation.country_name, nation.health_care_index])

    results = {'items': country_list}

    return jsonify(results)


@app.route("/crime_index.json", methods=["GET"])
def getCrimeIndex():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.crime_index:
            country_list.append([nation.country_name, nation.crime_index])

    results = {'items': country_list}

    return jsonify(results)


@app.route("/pollution_index.json", methods=["GET"])
def getPollutionIndex():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.pollution_index:
            country_list.append([nation.country_name, nation.pollution_index])

    results = {'items': country_list}

    return jsonify(results)


@app.route("/traffic_index.json", methods=["GET"])
def getTrafficIndex():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.traffic_index:
            country_list.append([nation.country_name, nation.traffic_index])

    results = {'items': country_list}

    return jsonify(results)


@app.route("/groceries_index.json", methods=["GET"])
def getGroceriesIndex():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.groceries_index:
            country_list.append([nation.country_name, nation.groceries_index])

    results = {'items': country_list}

    return jsonify(results)


@app.route("/rent_index.json", methods=["GET"])
def getRentIndex():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.rent_index:
            country_list.append([nation.country_name, nation.rent_index])

    results = {'items': country_list}

    return jsonify(results)



@app.route("/property_price_to_income_ratio.json", methods=["GET"])
def getPropertyPricetoIncome():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    for nation in nations: 
        if nation.property_price_to_income_ratio:
            country_list.append([nation.country_name, nation.property_price_to_income_ratio])

    results = {'items': country_list}

    return jsonify(results)
 

@app.route("/col_indexFilter.json", methods=["GET"])
def filterColIndex():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    max_val = request.args.get('filterMax')
    max_val = int(max_val)

    for nation in nations:
        if nation.col_index < max_val:
            country_list.append([nation.country_name, nation.col_index])

    results = {'items': country_list}

    return jsonify(results)



@app.route("/bread_priceFilter.json", methods=["GET"])
def filterBreadPrice():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    max_val = request.args.get('filterMax')
    max_val = int(max_val)

    for nation in nations:
        if nation.bread_price < max_val:
            country_list.append([nation.country_name, nation.bread_price])

    results = {'items': country_list}

    return jsonify(results)



@app.route("/meal_priceFilter.json", methods=["GET"])
def filterMealPrice():

    nations = Country.query.order_by('country_name').all()
    country_list = []

    max_val = request.args.get('filterMax')
    max_val = int(max_val)

    for nation in nations:
        if nation.meal_price < max_val:
            country_list.append([nation.country_name, nation.meal_price])

    results = {'items': country_list}

    return jsonify(results)


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
        q = q.filter(Country.meal_price < meal)

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



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
    
    app.run(port=5000, host='0.0.0.0')

