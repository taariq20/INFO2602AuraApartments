import os
from flask import Flask, render_template, url_for, jsonify, request, redirect, flash
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    JWTManager, create_access_token, get_jwt_identity, jwt_required,
    set_access_cookies, unset_jwt_cookies
)
from App.database import init_db, db  
from App.config import load_config
from App.controllers import setup_jwt, add_auth_context, get_current_user
from App.controllers.listing import listing_bp
from App.views import views, setup_admin
from App.models import User
from App.models.models import Listing
from App.models.user import Landlord

app = Flask(__name__, static_url_path='/static')

# JWT CONFIG FIX
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Replace with a real secret in production
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # For simplicity in testing


@app.route('/')
def index():
    import datetime
    current_year = datetime.datetime.now().year
    current_user = get_current_user()
    
    existing_user = Landlord.query.filter_by(username="landlord").first()
    if not existing_user:
        landlord = Landlord(username="landlord", password="password")
        db.session.add(landlord)
        db.session.commit()
        
    sample_listings = [
        Listing(title="Cozy Studio Apartment", description="Perfect for students", price=850, address="10 George Street", city="Port of Spain", landlord_id=1, image_url="/static/images/sampleapartment1.jpg"),
        Listing(title="Modern 2-Bedroom", description="New appliances, quiet neighborhood", price=1200, address="25 Oxford Avenue", city="Port of Spain", landlord_id=1, image_url="/static/images/sampleapartment2.jpg"),
        Listing(title="Downtown Condo", description="Close to campus and city center", price=1500, address="88 Port of Spain Blvd", city="Port of Spain", landlord_id=1, image_url="/static/images/sampleapartment3.jpg"),
    ]
    for listing in sample_listings:
        db.session.add(listing)

    db.session.commit()

    # Load all listings from DB
    all_listings = Listing.query.all()

    listings_with_ratings = []
    for listing in all_listings:
        reviews = listing.reviews
        if reviews:
            avg_rating = round(sum([r.rating for r in reviews]) / len(reviews), 1)
        else:
            avg_rating = 0
        listings_with_ratings.append((listing, avg_rating))

    featured = sorted(listings_with_ratings, key=lambda x: x[1], reverse=True)[:3]
    featured_apartments = [{'listing': f[0], 'average_rating': f[1]} for f in featured]

    return render_template(
        'index.html',
        current_year=current_year,
        featured_apartments=featured_apartments,
        all_listings=all_listings,
        current_user=current_user
    )


# User profile route (can be extended to show user listings, etc.)
@app.route('/profile', methods=['GET'])
@jwt_required()
def user_profile():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(
            username=user.username,
            email=user.email,
            listings=[listing.get_json() for listing in user.listings]  # Assuming User model has a relationship with listings
        )
    return jsonify(error="User not found"), 404


# Function to add views from blueprints
def add_views(app):
    for view in views:
        app.register_blueprint(view)

    app.register_blueprint(listing_bp, url_prefix='/listing')

def create_app(overrides={}):
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # You can enable this if you implement CSRF
    jwt = setup_jwt(app)
    setup_admin(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401

    app.app_context().push()
    return app
