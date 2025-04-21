from .user import create_user
from App.database import db
from App.models.user import Landlord

def initialize():
    db.drop_all()
    db.create_all()

    create_user('bob', 'bobpass')

    create_user('landlord1', 'landlordpass')
