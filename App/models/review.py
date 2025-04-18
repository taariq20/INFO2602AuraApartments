from App.database import db
from datetime import datetime



class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200))
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def __init__(self, rating, comment, tenant_id, listing_id):
    self.rating = rating
    self.comment = comment
    self.tenant_id = tenant_id
    self.listing_id = listing_id
