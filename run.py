from app import create_app
from app.models import URLModel
import os
from dotenv import load_dotenv

load_dotenv()

# Create Flask app
app = create_app()

# Initialize database
url_model = URLModel()
url_model.init_db()

if __name__ == '__main__':
    # Get configuration
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    
    # Run the app
    app.run(
        host='127.0.0.1',
        port=int(os.getenv('PORT', 5000)),
        debug=debug_mode
    )
