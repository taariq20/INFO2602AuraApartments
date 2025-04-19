from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))  

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
        
class Tenant(User):
    __tablename__ = 'tenant'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    reviews = db.relationship('Review', backref='tenant', lazy=True)
    __mapper_args__ = {
        'polymorphic_identity': 'tenant',
    }

class Landlord(User):
    __tablename__ = 'landlord'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    listings = db.relationship('Listing', backref='landlord', lazy=True)
    __mapper_args__ = {
        'polymorphic_identity': 'landlord',
    }

from App.models.models import Review
Tenant.reviews = db.relationship('Review', backref='tenant', lazy=True)