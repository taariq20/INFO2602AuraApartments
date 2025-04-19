from App.models import User
from App.database import db
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    
def get_current_user():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        print("User ID from JWT:", user_id, type(user_id))  # Debug line
        return User.query.get(int(user_id))  # ✅ Ensure it's an int
    except Exception as e:
        print(f"Error fetching current user: {e}")
        return None