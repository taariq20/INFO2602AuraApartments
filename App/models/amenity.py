from App.database import db



class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))

def __init__(self, name, listing_id):
    self.name = name
    self.listing_id = listing_id
