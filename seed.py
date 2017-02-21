import datetime
from sqlalchemy import func
from model import User, Country, connect_to_db, db
from server import app
import urllib2
import json 

def load_users():
    """Load users from u.user into travelers database."""

    # User.query.delete()

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


def load_1_usd_to_currency():

    """Load currency conversion data from Numbeo into travelers db"""

    url = 'https://www.numbeo.com/api/currency_exchange_rates?api_key=ps0u1c65ijsjqn'
    json_obj = urllib2.urlopen(url) 
    data = json.load(json_obj)

    for item in data['exchange_rates']:
        currency_per_USD = (item['one_usd_to_currency'])
        currency_code = item['currency']
        countries = Country.query.filter(Country.currency_code == currency_code).all()

        if countries: 
            for country in countries: 
                #sql magic that you can just put in country 
                country.currency_per_USD = currency_per_USD
                db.session.commit()
        else:
            pass 
        

def average_price(data, factor):

    """Calculate average price given a country and factors"""

    for dictionary in data['prices']:
        if factor in dictionary['item_name']:
            answer = dictionary
            return answer['average_price']


def load_cost_of_living():

    """Load cost of living data from Numbeo into travelers db"""

    # nations = ["Afghanistan","Aland Islands","Albania","Algeria","Andorra","Angola","Antigua And Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Bermuda","Bhutan","Bolivia","Bosnia And Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Croatia","Cuba","Curacao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Estonia","Ethiopia","Faroe Islands","Fiji","Finland","France","French Polynesia","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle Of Man","Israel","Italy","Ivory Coast","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kosovo (Disputed Territory)","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Lithuania","Luxembourg","Macao","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nepal","Netherlands","New Caledonia","New Zealand","Nicaragua","Nigeria","Northern Mariana Islands","Norway","Oman","Pakistan","Palestinian Territory","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Kitts And Nevis","Saint Lucia","Saint Vincent And The Grenadines","Samoa","Saudi Arabia","Senegal","Serbia","Seychelles","Singapore","Sint Maarten","Slovakia","Slovenia","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tonga","Trinidad And Tobago","Tunisia","Turkey","Turkmenistan","Turks And Caicos Islands","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Us Virgin Islands","Uzbekistan","Vanuatu","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]

    nations = ["Afghanistan","Aland Islands","Albania"]

    for nation in nations:

        try:
            url = 'https://www.numbeo.com/api/country_prices?api_key=ps0u1c65ijsjqn&country='
            #look up URL encoding library 
            url = url + nation.replace(" ", "+") + '&currency=USD'
            print "URL in try loop", url 
            #consider saving file locally bc this might be whats takng a long time
            #look up processing timing libraries 
            json_obj = urllib2.urlopen(url)
            data = json.load(json_obj)
           
            apt_price = average_price(data, "Apartment (1 bedroom) in City Centre, Rent Per Month")
            meal_price = average_price(data, "Meal, Inexpensive Restaurant, Restaurants")
            bread_price = average_price(data, "Fresh White Bread (500g)")

            countries = Country.query.filter(Country.country_name == nation).all()

            if countries: 
                for country in countries: 
                    country.apt_price = apt_price
                    country.meal_price = meal_price
                    country.bread_price = bread_price
                    # db.session.commit()
                else:
                    pass 
        except: 
            pass 


def load_cost_of_living_index():
    
    nations = ["Afghanistan","Aland Islands","Albania","Algeria","Andorra","Angola","Antigua And Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Bermuda","Bhutan","Bolivia","Bosnia And Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Croatia","Cuba","Curacao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Estonia","Ethiopia","Faroe Islands","Fiji","Finland","France","French Polynesia","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle Of Man","Israel","Italy","Ivory Coast","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kosovo (Disputed Territory)","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Lithuania","Luxembourg","Macao","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nepal","Netherlands","New Caledonia","New Zealand","Nicaragua","Nigeria","Northern Mariana Islands","Norway","Oman","Pakistan","Palestinian Territory","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Kitts And Nevis","Saint Lucia","Saint Vincent And The Grenadines","Samoa","Saudi Arabia","Senegal","Serbia","Seychelles","Singapore","Sint Maarten","Slovakia","Slovenia","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tonga","Trinidad And Tobago","Tunisia","Turkey","Turkmenistan","Turks And Caicos Islands","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Us Virgin Islands","Uzbekistan","Vanuatu","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]

    for nation in nations:

        try:
            url = 'https://www.numbeo.com/api/country_indices?api_key=ps0u1c65ijsjqn&country='
            url = url + nation.replace(" ", "+")
            print "URL in try loop", url 
            json_obj = urllib2.urlopen(url)
            data = json.load(json_obj)
            col_index= data['cpi_index']

            countries = Country.query.filter(Country.country_name == nation).all()

            if countries: 
                for country in countries: 
                    country.col_index = col_index 
                    db.session.commit()
        except: 
            pass 


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
    # load_cost_of_living_index()
    load_numbeo_data(col_url, '&currency=USD')
    load_numbeo_data(col_index_url)

   #can also seed country_searches table if desired

   