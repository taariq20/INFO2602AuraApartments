from App.models import *
from App.database import db





def create_amenity(name, listing_id):
    amenity = Amenity(name, listing_id)
    db.session.add(amenity)
    db.session.commit()
    return amenity
