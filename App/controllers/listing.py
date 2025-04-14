from App.models import *
from App.database import db



def create_listing(title, description, address, city, price, landlord_id, image_url=None):
    listing = Listing(title, description, address, city, price, landlord_id, image_url)
    db.session.add(listing)
    db.session.commit()
    return listing

def to_dict(self):
    return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "address": self.address,
        "city": self.city,
        "price": self.price,
        "image_url": self.image_url,
        "landlord_id": self.landlord_id,
        "amenities": [a.name for a in self.amenities]
    }
