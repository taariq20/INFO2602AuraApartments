from App.database import db



class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
