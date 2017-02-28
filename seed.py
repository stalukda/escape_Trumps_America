import datetime
from sqlalchemy import func
from model import User, Country, connect_to_db, db
from server import app
from nations import nations
import urllib2
import json 
import requests
import csv

def load_users():
    """Load users from u.user into travelers database."""

    print "Users"

    for i, row in enumerate(open("seed_data/u.user")):
        print "Seeding entry #: ", i 
        row = row.rstrip()
        fname, lname, email, password, age, zipcode, home_country = row.split("|")

        user = User(fname=fname,
                    lname=lname,
                    email=email,
                    password=password,
                    age=age,
                    zipcode=zipcode,
                    home_country=home_country)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    db.session.commit()


def load_currency():

    """Load country & currency data from u.country into travelers db"""

    for i, row in enumerate(open("seed_data/u.country_code")):
        row = row.rstrip()
        country_name, country_code, currency_name, currency_code = row.split(",")
        
        country = Country(country_name=country_name,
            country_code=country_code,
            currency_name=currency_name,
            currency_code=currency_code)

        db.session.add(country)
    db.session.commit()


def url_to_json(url, parameters):
    try:
        r = requests.get(url, params=parameters)
        data = r.json()
        return data
    except: 
        pass #add in error log 


def load_1_usd_to_currency():

    """Load currency conversion data from Numbeo into travelers db"""

    data = url_to_json('https://www.numbeo.com/api/currency_exchange_rates', {'api_key': 'ps0u1c65ijsjqn'})

    for item in data['exchange_rates']:
        currency_per_USD = (item['one_usd_to_currency'])
        currency_code = item['currency']
        print "currency_code", currency_code
        
        countries = Country.query.filter(Country.currency_code == currency_code).all()

        if countries: 
            for country in countries:
                country.currency_per_USD = currency_per_USD
                db.session.commit()
        

def average_price(data, factor):

    """Calculate average price given a country and factors"""

    for dictionary in data['prices']:
        if factor in dictionary['item_name']:
            answer = dictionary
            print "average price: ", answer['average_price']
            return answer['average_price']


def load_cost_of_living():

    """Load cost of living data from Numbeo into travelers db"""

    for nation in nations:

        data = url_to_json('https://www.numbeo.com/api/country_prices', {'api_key': 'ps0u1c65ijsjqn', 'country': nation, 'currency': 'USD'}) 
        apt_price = average_price(data, "Apartment (1 bedroom) in City Centre, Rent Per Month")
        meal_price = average_price(data, "Meal, Inexpensive Restaurant, Restaurants")
        bread_price = average_price(data, "Fresh White Bread (500g)")

        countries = Country.query.filter(Country.country_name == nation).all()

        if countries: 
            for country in countries: 
                country.apt_price = apt_price
                country.meal_price = meal_price
                country.bread_price = bread_price
                db.session.commit()

  
def load_cost_of_living_index():

    for nation in nations:

        data = url_to_json('https://www.numbeo.com/api/country_indices', {'api_key': 'ps0u1c65ijsjqn', 'country': nation}) 
        try: 
            quality_of_life_index = data['quality_of_life_index']
            # col_index = data['cpi_index']
            # health_care_index = data['health_care_index']
            # crime_index = data['crime_index']
            # pollution_index = data['pollution_index']
            # traffic_index = data['traffic_index']
            # groceries_index = data['groceries_index']
            # rent_index = data['rent_index']
            # property_price_to_income_ratio = data['property_price_to_income_ratio']

        except: 
            print nation #log to error log 

        countries = Country.query.filter(Country.country_name == nation).all()

        if countries: 
            for country in countries: 
                # country.col_index = col_index 
                # country.health_care_index = health_care_index
                # country.crime_index = crime_index
                # country.pollution_index = pollution_index
                # country.traffic_index = traffic_index
                # country.groceries_index = groceries_index
                # country.rent_index = rent_index
                # country.property_price_to_income_ratio = property_price_to_income_ratio
                country.quality_of_life_index = quality_of_life_index # not working for some reason 
                db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

   #seed users table 
    # load_users()
    # set_val_user_id()

   #seed countries table 
    # load_currency()
    # load_1_usd_to_currency()
    # load_cost_of_living()
    load_cost_of_living_index()

   #can also seed country_searches table if desired

   