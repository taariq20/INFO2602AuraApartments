from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.controllers.user import get_all_users
from App.controllers import login, register_user
from App.models.user import User

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''    
@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    
@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    
    if not token:
        flash('Bad username or password given', 'error')
        return redirect(url_for('auth_views.login_page'))  # Stay on login page on failure
    
    response = redirect(url_for('index'))  # Redirect to homepage on success
    flash('Login Successful', 'success')
    set_access_cookies(response, token)
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!", 'success')
    unset_jwt_cookies(response)
    return response

@auth_views.route('/signup', methods=['POST'])
def signup_route():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type', 'tenant')

    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'error')
        return redirect(request.referrer)

    user = register_user(username, password, user_type)
    if user:
        token = login(username, password)
        response = redirect(url_for('index'))
        flash('Signup successful!', 'success')
        set_access_cookies(response, token)
        return response

    flash('Error creating user', 'error')
    return redirect(request.referrer)

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    token = login(data['username'], data['password'])
    if not token:
        return jsonify(message='bad username or password given'), 401
    response = jsonify(access_token=token) 
    set_access_cookies(response, token)
    return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = redirect(url_for('index'))
    flash("Logged out successfully!", "success")
    unset_jwt_cookies(response)
    return response