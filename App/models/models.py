from datetime import datetime
from App.database import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200))
    
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'))  # Link specifically to Tenant
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, rating, comment, tenant_id, listing_id):
        self.rating = rating
        self.comment = comment
        self.tenant_id = tenant_id
        self.listing_id = listing_id

    def get_json(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'tenant_id': self.tenant_id,
            'listing_id': self.listing_id,
            'created_at': self.created_at
        }

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))

    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)

    amenities = db.relationship('Amenity', backref='listing', lazy=True)
    reviews = db.relationship('Review', backref='listing', lazy=True)

    def __init__(self, title, description, address, city, price, landlord_id, image_url=None):
        self.title = title
        self.description = description
        self.address = address
        self.city = city
        self.price = price
        self.landlord_id = landlord_id
        self.image_url = image_url

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'price': self.price,
            'image_url': self.image_url,
            'landlord_id': self.landlord_id,
            'amenities': [a.get_json() for a in self.amenities],
            'reviews': [r.get_json() for r in self.reviews]
        }

    def is_added_by_user(self, user_id):
        return self.landlord_id == user_id

class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))

    def __init__(self, name, listing_id):
        self.name = name
        self.listing_id = listing_id

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'listing_id': self.listing_id
        }
