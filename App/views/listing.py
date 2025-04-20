from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers import (
    create_listing,
    get_all_listings,
    get_all_listings_json,
    create_review,
    get_reviews_by_listing_id,
    create_amenity,
    get_listing_by_id
)

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

@listing_views.route('/listings', methods=['POST'])
@jwt_required()
def create_listing_action():
    data = request.form
    create_listing(
        title=data['title'],
        description=data['description'],
        address=data['address'],
        city=data['city'],
        price=float(data['price']),
        landlord_id=jwt_current_user.id,
        image_url=data.get('image_url')
    )
    flash("Listing created!")
    return redirect(url_for('listing_views.get_listing_page'))


@listing_views.route('/api/listings', methods=['GET'])
def get_listings_api():
    return jsonify(get_all_listings_json())


@listing_views.route('/api/listings', methods=['POST'])
@jwt_required()
def create_listing_api():
    data = request.json
    listing = create_listing(
        title=data['title'],
        description=data['description'],
        address=data['address'],
        city=data['city'],
        price=float(data['price']),
        landlord_id=jwt_current_user.id,
        image_url=data.get('image_url')
    )
    return jsonify({'message': f'Listing {listing.title} created with ID {listing.id}'})


@listing_views.route('/listings/<int:listing_id>/review', methods=['POST'])
@jwt_required()
def create_review_action(listing_id):
    data = request.form
    create_review(
        rating=int(data['rating']),
        comment=data['comment'],
        tenant_id=jwt_current_user.id,
        listing_id=listing_id
    )
    flash("Review submitted!")
    return redirect(url_for('listing_views.get_listing_page'))


@listing_views.route('/listings/<int:listing_id>', methods=['GET'])
def listing_detail_page(listing_id):
    listing = get_listing_by_id(listing_id)
    reviews = get_reviews_by_listing_id(listing_id)
    return render_template('listing_detail.html', listing=listing, reviews=reviews)


@listing_views.route('/api/amenities', methods=['POST'])
@jwt_required()
def create_amenity_api():
    data = request.json
    amenity = create_amenity(data['name'], data['listing_id'])
    return jsonify({'message': f"Amenity '{amenity.name}' added to listing {amenity.listing_id}"})
