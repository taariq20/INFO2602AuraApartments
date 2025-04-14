from App.database import db



class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(300))
    
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
