from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Country, Country_Search


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

    user_id = session.get("user_id")
    
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
    else:
        pass 

    nations = request.args.getlist('countries')
    country_info = []

    for nation in nations: 
        url = "https://www.kiva.org/lend?country="
        #check each nation picked against the db 
        country = Country.query.filter_by(country_name=nation).first()
        
        if country: 
            country_with_urls = {}
            country_with_urls[country] = url + country.country_code
            country_info.append(country_with_urls)
        else: 
            pass 

    return render_template("country_display.html", country_info=country_info, user=user)
   


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
    
    app.run(port=5000, host='0.0.0.0')

