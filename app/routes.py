from flask import Blueprint, request, redirect, jsonify, render_template
from .services import URLShortenerService
import os

main_bp = Blueprint('main', __name__)
service = URLShortenerService()

@main_bp.route('/', methods=['GET'])
def index():
    """Serve the index page"""
    return render_template('index.html')

@main_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'url-shortener',
        'version': '1.0.0'
    }), 200

@main_bp.route('/shorten', methods=['POST'])
def shorten():
    """Create a shortened URL"""
    try:
        data = request.get_json()
        original_url = data.get('url') or data.get('original_url')
        
        if not original_url:
            return jsonify({'error': 'URL is required'}), 400
        
        result = service.shorten_url(original_url)
        
        if not result:
            return jsonify({'error': 'Failed to create short URL'}), 500
        
        base_url = os.getenv('BASE_URL', f"{request.host_url.rstrip('/')}")
        short_url = f"{base_url}/{result['short_code']}"
        
        return jsonify({
            'id': result['id'],
            'long_url': result['original_url'],
            'short_code': result['short_code'],
            'short_url': short_url,
            'created_at': str(result['created_at']),
            'click_count': result['clicks']
        }), 201
    
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@main_bp.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    """Redirect to original URL"""
    try:
        original_url = service.get_original_url(short_code)
        
        if not original_url:
            return jsonify({'error': 'URL not found'}), 404
        
        return redirect(original_url, code=301)
    
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@main_bp.route('/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    """Get URL statistics"""
    try:
        stats = service.get_stats(short_code)
        
        if not stats:
            return jsonify({'error': 'URL not found'}), 404
        
        return jsonify({
            'id': stats['id'],
            'long_url': stats['original_url'],
            'short_code': stats['short_code'],
            'created_at': str(stats['created_at']),
            'click_count': stats['clicks']
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
