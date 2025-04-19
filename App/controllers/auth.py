from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models.user import User, Landlord, Tenant
from App.database import db

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=str(user.id))  # ✅ send user ID as string
    return None


def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        return str(user_id)  

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(str(identity)) 

    return jwt  


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        is_authenticated = True if current_user else False
        print(f"JWT user ID: {user_id}, Authenticated: {is_authenticated}")
    except Exception as e:
        print(f"Error in inject_user: {e}")
        is_authenticated = False
        current_user = None
    return dict(is_authenticated=is_authenticated, current_user=current_user)

def register_user(username, password, user_type='tenant'):
    try:
        if user_type.lower() == 'landlord':
            user = Landlord(username, password)
        else:
            user = Tenant(username, password)
        
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        print(f"Error registering user: {e}")
        return None
        
def get_current_user():
    """Get the current logged in user"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except Exception as e:
        return None