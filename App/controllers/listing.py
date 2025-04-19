# App/controllers/listing.py

from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.models.models import Listing, Amenity, Review
from App.models.user import Landlord, Tenant
from App.database import db
from App.models.user import User

listing_bp = Blueprint('listing', __name__)

# Modify the add_listing route in listing.py
@listing_bp.route('/add', methods=['POST'])
@jwt_required()  # Use JWT instead of session
def add_listing():
    # Get current user ID from JWT
    user_id = get_jwt_identity()
    
    if not user_id:
        flash("You must be logged in to add a listing", "error")
        return redirect(url_for('index'))
    
    user = User.query.get(user_id)
    if not user:
        flash("User not found", "error")
        return redirect(url_for('index'))
    
    # Check if user is a landlord
    if user.type != 'landlord':
        flash("Only landlords can add listings", "error")
        return redirect(url_for('index'))
    
    title = request.form.get('title')
    description = request.form.get('description')
    address = request.form.get('address')
    city = request.form.get('city')
    price = request.form.get('price')
    image_url = request.form.get('image_url')
    
    # Validate required fields
    if not all([title, description, address, city, price]):
        flash("Missing required fields", "error")
        return redirect(url_for('index'))
    
    try:
        # Create new listing
        new_listing = Listing(
            title=title,
            description=description,
            address=address,
            city=city,
            price=float(price),
            landlord_id=user_id,
            image_url=image_url
        )
        
        db.session.add(new_listing)
        db.session.commit()
        
        # Add amenities if provided
        amenities = request.form.getlist('amenities')
        if amenities:
            for amenity_name in amenities:
                amenity = Amenity(name=amenity_name, listing_id=new_listing.id)
                db.session.add(amenity)
            db.session.commit()
        
        flash("Listing added successfully!", "success")
        return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding listing: {str(e)}", "error")
        return redirect(url_for('index'))
    
@listing_bp.route('/remove/<int:listing_id>', methods=['POST'])
@jwt_required()
def remove_listing(listing_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    listing = Listing.query.get(listing_id)
    if not listing:
        flash("Listing not found", "error")
        return redirect(url_for('index'))

    # Ensure the user is a landlord and owns the listing
    if not isinstance(user, Landlord) or listing.landlord_id != user.id:
        flash("You can only delete your own listings", "error")
        return redirect(url_for('listing.view_listing', listing_id=listing_id))

    try:
        db.session.delete(listing)
        db.session.commit()
        flash("Listing removed successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error removing listing: {str(e)}", "error")

    return redirect(url_for('index'))


@listing_bp.route('/get-listings')
def get_listings():
    listings = Listing.query.all()
    return jsonify([listing.get_json() for listing in listings])

@listing_bp.route('/my-listings')
def my_listings():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session['user_id']
    user_listings = Listing.query.filter_by(landlord_id=user_id).all()
    return jsonify([listing.get_json() for listing in user_listings])

@listing_bp.route('/<int:listing_id>/review', methods=['POST'])
@jwt_required()
def add_review(listing_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or user.type != 'tenant':
        flash("Only tenants can leave reviews", "error")
        return redirect(url_for('listing.view_listing', listing_id=listing_id))

    rating = int(request.form.get('rating'))
    comment = request.form.get('text')

    new_review = Review(
        rating=rating,
        comment=comment,
        tenant_id=user.id,
        listing_id=listing_id
    )
    db.session.add(new_review)
    db.session.commit()

    flash("Review submitted successfully!", "success")
    return redirect(url_for('listing.view_listing', listing_id=listing_id))

@listing_bp.route('/<int:listing_id>/review/<int:review_id>/delete', methods=['POST'])
@jwt_required()
def delete_review(listing_id, review_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    review = Review.query.get_or_404(review_id)

    # Ensure only the tenant who wrote the review can delete it
    if not isinstance(current_user, Tenant) or review.tenant_id != current_user.id:
        flash("You can only delete your own reviews.", "error")
        return redirect(url_for('listing.view_listing', listing_id=listing_id))

    db.session.delete(review)
    db.session.commit()
    flash("Review deleted successfully.", "success")
    return redirect(url_for('listing.view_listing', listing_id=listing_id))

@listing_bp.route('/<int:listing_id>')
def view_listing(listing_id):
    from App.models.models import Listing, Review
    from App.database import db

    listing = Listing.query.get(listing_id)
    if not listing:
        return f"Listing {listing_id} not found.", 404

    reviews = Review.query.filter_by(listing_id=listing.id).order_by(Review.created_at.desc()).all()
    return render_template('listing_detail.html', listing=listing, reviews=reviews)

