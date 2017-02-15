from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Country


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    user = User.query.filter_by(email=email).first()

    if not user:
        new_user = User(fname=fname, lname=lname, email=email, password=password, age=age, zipcode=zipcode)
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

    # Get form variables
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

    return render_template("search_button.html")


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

    return render_template("pick_countries.html")


@app.route("/compare_countries", methods=["GET"])
def compare_countries():
    """Compare the 3-5 chosen countries"""

    # rebinding the user's picked countries to the nation variable 
    nations = request.args.getlist('countries')
    nations_to_display = []
    urls_to_display = []

    for nation in nations: 
        url = "https://www.kiva.org/lend?country="
        #check each nation picked against the db 
        country = Country.query.filter_by(country_name=nation).first()
        if country: 
            url = url + country.country_code
            urls_to_display.append(url) 
            nations_to_display.append(country)
        else: 
            pass 


    return render_template("country_display.html", nations=nations_to_display, urls_to_display=urls_to_display)

    # nations = request.args.getlist('countries')
    # nations_to_display = []

    # for nation in nations: 
    #     url = "https://www.kiva.org/lend?country="
    #     #check each nation picked against the db 
    #     country = Country.query.filter_by(country_name=nation).first()
    #     if country: 
    #         #add the url + nation to country_info... lots of little dictionaries to put
    #         #into the list 
    #         country_info = {}
    #         country_info[country] = url + country.country_code
    #         nations_to_display.append(country_info)
    #     else: 
    #         pass 

    # return render_template("country_display.html", nations=nations_to_display)
   


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
    
    app.run(port=5000, host='0.0.0.0')



# @app.route("/movies/<int:movie_id>", methods=['GET'])
# def movie_detail(movie_id):
#     """Show info about movie.

#     If a user is logged in, let them add/edit a rating.
#     """

#     movie = Movie.query.get(movie_id)

#     user_id = session.get("user_id")

#     if user_id:
#         user_rating = Rating.query.filter_by(
#             movie_id=movie_id, user_id=user_id).first()

#     else:
#         user_rating = None

#     return render_template("movie.html",
#                            movie=movie,
#                            user_rating=user_rating)


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def movie_detail_process(movie_id):
#     """Add/edit a rating."""

#     # Get form variables
#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("No user logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash("Rating updated.")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Rating added.")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)
