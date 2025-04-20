from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
from App.models.models import Listing

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get search query from the URL parameter
    listing = None
    error_message = None

    if query:
        # Search for a single listing by title or city
        listing = Listing.query.filter(
            Listing.title.ilike(f'%{query}%') | Listing.city.ilike(f'%{query}%')
        ).first()  # Fetch only the first matching listing
        
        if not listing:
            # If no listing is found, set an error message
            error_message = f'No listings found for "{query}".'

    # Return the index page with search results or error message
    return render_template('index.html', listing=listing, error_message=error_message, query=query)
