"""Models and database functions for The Guilty Traveler project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of The Guilty Traveler website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(64), nullable=True)
    lname = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    ## model on one to many relationship for backref (printings & books)
    home_country = db.Column(db.String(15), db.ForeignKey('countries.country_code'), nullable=True)

    def __repr__(self):
        return "<User user_id=%s fname=%s lname=%s home_country=%s>" % (self.user_id,
                                               self.fname,
                                               self.lname, 
                                               self.home_country)

class Country(db.Model):
    """Countries to display on the website."""

    __tablename__ = "countries"

    country_code = db.Column(db.String(2),
                         primary_key=True)
    country_name = db.Column(db.String(100), nullable=True)
    currency_code = db.Column(db.String(3), nullable=True)
    currency_name = db.Column(db.String(64), nullable=True)
    currency_per_USD = db.Column(db.Integer, nullable=True)
    bread_price = db.Column(db.Integer, nullable=True)
    meal_price = db.Column(db.Integer, nullable=True)
    apt_price = db.Column(db.Integer, nullable=True)

    def __repr__(self):

        return "<Country country_name=%s currency_name=%s>" % (self.country_name,
                                                                self.currency_name)


## Potentially country_search in the future (to store the multiple countries that a user would be interested in saving)

class Country_Search(db.Model):
    """Countries to display on the website."""

    __tablename__ = "country_searches"

    uc_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    country_code = db.Column(db.String(2), db.ForeignKey('countries.country_code'), nullable=True)

    user = db.relationship("User", backref=db.backref("country_searches", order_by=uc_id))
    country = db.relationship("Country", backref=db.backref("country_searches", order_by=uc_id))

    def __repr__(self):

        return "<Country_Search uc_id=%s>" % (self.uc_id)



#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///travelers'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
