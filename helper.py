from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Country, Country_Search
from sqlalchemy import desc, func
import json 
import flickrapi
import os

def flickr_pics(country_name):
    """
    Provide picture to display for each country. 

    >>> flickr_pics("France")
    'https://farm1.staticflickr.com/743/33097816880_984e43bf0c.jpg'"""

    #TODO - get this into my secrets.sh file - figure out how to uniode it in .sh
    api_key = u'9489272c64643fc71165347fccfebbc0'
    api_secret = u'81789d543c6d0977'

    # api_key = os.environ['api_key']
    # print "API KEY: ", api_key
    # api_secret = os.environ['api_secret']

    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    country = "landmark" + " " + country_name 
    photo = flickr.photos.search(per_page='1', format='json', text=country, accuracy=3, safe_search=1, content_type=1)
    print "this is photo: ", photo
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

def process_country_factor(factor): 
    nations = Country.query.order_by("country_name").all()
    country_list = []

    for nation in nations: 
        if factor == "col_index":
            country_list.append([nation.country_name, nation.col_index])
        elif factor == "meal_price":
            country_list.append([nation.country_name, nation.meal_price])
        elif factor == "bread_price": 
            country_list.append([nation.country_name, nation.bread_price])
        elif factor == "apt_price": 
            country_list.append([nation.country_name, nation.apt_price])
        elif factor == "health_care_index": 
            country_list.append([nation.country_name, nation.health_care_index])
        elif factor == "crime_index": 
            country_list.append([nation.country_name, nation.crime_index])
        elif factor == "pollution_index": 
            country_list.append([nation.country_name, nation.pollution_index])
        elif factor == "traffic_index": 
            country_list.append([nation.country_name, nation.traffic_index])
        elif factor == "groceries_index": 
            country_list.append([nation.country_name, nation.groceries_index])
        elif factor == "rent_index": 
            country_list.append([nation.country_name, nation.rent_index])
        elif factor == "property_price_to_income_ratio": 
            country_list.append([nation.country_name, nation.property_price_to_income_ratio])

    results = {'items': country_list}
    return results


#To finish building
def process_multiple_country_factors(): 

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

    return results