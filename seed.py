import datetime
from sqlalchemy import func
from model import User, Country, connect_to_db, db
from server import app
import urllib2
import json 

def load_users():
    """Load users from u.user into database."""

    User.query.delete()

    print "Users"

    for i, row in enumerate(open("seed_data/u.user")):
        print "Seeding entry #: ", i 
        row = row.rstrip()
        fname, lname, email, password, age, zipcode = row.split("|")

        user = User(fname=fname,
                    lname=lname,
                    email=email,
                    password=password,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()

# bangladesh = Country(country_code='BD', country_name='Bangladesh', currency_code='TK', currency_name='Taka', currency_per_USD=70, bread_price=1, meal_price=2, apt_price=3)

def country_to_country_code():

    Country.query.delete()

    for i, row in enumerate(open("seed_data/u.country_code")):
        row = row.rstrip()
        country_name, country_code, currency_name, currency_code = row.split(",")
        
        country = Country(country_name=country_name,
            country_code=country_code,
            currency_name=currency_name,
            currency_code=currency_code)

        db.session.add(country)
    db.session.commit()

def usd_to_currency():

    url = 'https://www.numbeo.com/api/currency_exchange_rates?api_key=ps0u1c65ijsjqn'
    json_obj = urllib2.urlopen(url) 
    data = json.load(json_obj)

    for item in data['exchange_rates']:
        currency_per_USD = (item['one_usd_to_currency'])
        currency_code = item['currency']
        # if the currency name is the same as the currency name in the database

        countries = Country.query.filter(Country.currency_code == currency_code).all()

        if countries: 
            for country in countries: 
                country.currency_per_USD = currency_per_USD
                db.session.commit()
        else:
            pass 
        



# def load_countries():
#     """Load movies from u.item into database."""

# # bangladesh = Country(country_code='BD', country_name='Bangladesh', currency_code='TK', currency_name='Taka', currency_per_USD=70, bread_price=1, meal_price=2, apt_price=3)

# # db.session.add(bangladesh)
# # db.session.commit()

#     print "Countries"
#     country_to_country_code()





    # for i, row in enumerate():
    #     row = row.rstrip()

    #     # clever -- we can unpack part of the row!
    #     countries  = row.split("|")
    #     print countries

    #     The date is in the file as daynum-month_abbreviation-year;
    #     we need to convert it to an actual datetime object.

    #     if released_str:
    #         released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
    #     else:
    #         released_at = None

    #     # Remove the (YEAR) from the end of the title.

    #     title = title[:-7]   # " (YEAR)" == 7

    #     movie = Movie(movie_id=movie_id,
    #                   title=title,
    #                   released_at=released_at,
    #                   imdb_url=imdb_url)

    #     # We need to add to the session or it won't ever be stored
    #     db.session.add(movie)

    #     # provide some sense of progress
    #     if i % 100 == 0:
    #         print i

    # # Once we're done, we should commit our work
    # db.session.commit()


# def load_ratings():
#     """Load ratings from u.data into database."""

#     print "Ratings"

#     for i, row in enumerate(open("seed_data/u.data")):
#         row = row.rstrip()

#         user_id, movie_id, score, timestamp = row.split("\t")

#         user_id = int(user_id)
#         movie_id = int(movie_id)
#         score = int(score)

#         # We don't care about the timestamp, so we'll ignore this

#         rating = Rating(user_id=user_id,
#                         movie_id=movie_id,
#                         score=score)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(rating)

#         # provide some sense of progress
#         if i % 1000 == 0:
#             print i

#             # An optimization: if we commit after every add, the database
#             # will do a lot of work committing each record. However, if we
#             # wait until the end, on computers with smaller amounts of
#             # memory, it might thrash around. By committing every 1,000th
#             # add, we'll strike a good balance.

#             db.session.commit()

#     # Once we're done, we should commit our work
#     db.session.commit()


# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # load_users()
    # load_countries()
    # load_ratings()
    # set_val_user_id()
    country_to_country_code()
    usd_to_currency()

    # # Mimic what we did in the interpreter, and add the Eye and some ratings
    # eye = User(email="the-eye@of-judgment.com", password="evil")
    # db.session.add(eye)
    # db.session.commit()

    # # Toy Story
    # r = Rating(user_id=eye.user_id, movie_id=1, score=1)
    # db.session.add(r)

    # # Robocop 3
    # r = Rating(user_id=eye.user_id, movie_id=1274, score=5)
    # db.session.add(r)

    # # Judge Dredd
    # r = Rating(user_id=eye.user_id, movie_id=373, score=5)
    # db.session.add(r)

    # # 3 Ninjas
    # r = Rating(user_id=eye.user_id, movie_id=314, score=5)
    # db.session.add(r)

    # # Aladdin
    # r = Rating(user_id=eye.user_id, movie_id=95, score=1)
    # db.session.add(r)

    # # The Lion King
    # r = Rating(user_id=eye.user_id, movie_id=71, score=1)
    # db.session.add(r)

    # db.session.commit()
    
    # # Add our user
    # jessica = User(email="jessica@gmail.com",
    #                password="love",
    #                age=42,
    #                zipcode="94114")
    # db.session.add(jessica)
    # db.session.commit()

    # # Toy Story
    # r = Rating(user_id=jessica.user_id, movie_id=1, score=5)
    # db.session.add(r)

    # # Robocop 3
    # r = Rating(user_id=jessica.user_id, movie_id=1274, score=1)
    # db.session.add(r)

    # # Judge Dredd
    # r = Rating(user_id=jessica.user_id, movie_id=373, score=1)
    # db.session.add(r)

    # # 3 Ninjas
    # r = Rating(user_id=jessica.user_id, movie_id=314, score=1)
    # db.session.add(r)

    # # Aladdin
    # r = Rating(user_id=jessica.user_id, movie_id=95, score=5)
    # db.session.add(r)

    # # The Lion King
    # r = Rating(user_id=jessica.user_id, movie_id=71, score=5)
    # db.session.add(r)

    # db.session.commit()
