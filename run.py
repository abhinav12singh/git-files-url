from app import create_app
from app.models import URLModel
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

with app.app_context():
    url_model = URLModel()
    url_model.init_db()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_ENV") == "development"
    )