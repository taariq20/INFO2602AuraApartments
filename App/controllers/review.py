from App.models import *
from App.database import db



def create_review(rating, comment, tenant_id, listing_id):
    review = Review(rating, comment, tenant_id, listing_id)
    db.session.add(review)
    db.session.commit()
    return review

def to_dict(self):
    return {
        "id": self.id,
        "rating": self.rating,
        "comment": self.comment,
        "tenant_id": self.tenant_id,
        "listing_id": self.listing_id,
        "created_at": self.created_at.isoformat()
    }
