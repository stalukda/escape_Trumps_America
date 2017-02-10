import urllib2
import json 



def average_price(data, factor):
    for dictionary in data['prices']:
        if factor in dictionary['item_name']:
            answer = dictionary
            return answer['average_price']


def per_country():

    countries = ["Afghanistan","Aland Islands","Albania","Algeria","Andorra","Angola","Antigua And Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Bermuda","Bhutan","Bolivia","Bosnia And Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Croatia","Cuba","Curacao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Estonia","Ethiopia","Faroe Islands","Fiji","Finland","France","French Polynesia","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle Of Man","Israel","Italy","Ivory Coast","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kosovo (Disputed Territory)","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Lithuania","Luxembourg","Macao","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nepal","Netherlands","New Caledonia","New Zealand","Nicaragua","Nigeria","Northern Mariana Islands","Norway","Oman","Pakistan","Palestinian Territory","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Kitts And Nevis","Saint Lucia","Saint Vincent And The Grenadines","Samoa","Saudi Arabia","Senegal","Serbia","Seychelles","Singapore","Sint Maarten","Slovakia","Slovenia","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tonga","Trinidad And Tobago","Tunisia","Turkey","Turkmenistan","Turks And Caicos Islands","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Us Virgin Islands","Uzbekistan","Vanuatu","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]

    for country in countries:

        url = 'https://www.numbeo.com/api/country_prices?api_key=ps0u1c65ijsjqn&country='
        
        try:
            url = url + country.replace(" ", "+") + '&currency=USD' 
            json_obj = urllib2.urlopen(url) 
            data = json.load(json_obj)
            apt_price = average_price(data, "Apartment (1 bedroom) in City Centre, Rent Per Month")
            meal_price = average_price(data, "Meal, Inexpensive Restaurant, Restaurants")
            bread_price = average_price(data, "Fresh White Bread (500g)")
        except: 
            pass 

per_country()









# def country_to_country_code():
#     for i, row in enumerate(open("seed_data/u.country_code")):
#         row = row.rstrip()
#         country, country_code, currency, currency_code = row.split(",")
#         print country_code, i  

# country_to_country_code()


# def usd_to_currency():
#     url = 'https://www.numbeo.com/api/currency_exchange_rates?api_key=ps0u1c65ijsjqn'
#     json_obj = urllib2.urlopen(url) 
#     data = json.load(json_obj)

#     for item in data['exchange_rates']:
#         print "One US dollar is worth {:} in {:}.".format(item['one_usd_to_currency']
#               , item['currency'])

def usd_to_currency():
    url = 'https://www.numbeo.com/api/currency_exchange_rates?api_key=ps0u1c65ijsjqn'
    json_obj = urllib2.urlopen(url) 
    data = json.load(json_obj)

    for item in data['exchange_rates']:
        currency_per_USD = item['one_usd_to_currency']
        currency_name = item['currency']


