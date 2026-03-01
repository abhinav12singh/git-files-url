import psycopg2
from psycopg2.extras import RealDictCursor
import os

class URLModel:
    """Database model for URL shortcuts"""
    
    def __init__(self, db_url=None):
        self.db_url = db_url or os.getenv('DATABASE_URL')
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.db_url)
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id SERIAL PRIMARY KEY,
                short_code VARCHAR(10) UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                clicks INT DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Create index on short_code for faster lookups
        cur.execute('''
            CREATE INDEX IF NOT EXISTS idx_urls_short_code 
            ON urls(short_code)
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
    
    def create_url(self, short_code, original_url):
        """Create a new shortened URL"""
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute(
                '''INSERT INTO urls (short_code, original_url) 
                   VALUES (%s, %s) RETURNING *''',
                (short_code, original_url)
            )
            result = cur.fetchone()
            conn.commit()
            return dict(result) if result else None
        except psycopg2.IntegrityError:
            conn.rollback()
            return None
        finally:
            cur.close()
            conn.close()
    
    def get_url_by_code(self, short_code):
        """Get URL by short code"""
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute(
            'SELECT * FROM urls WHERE short_code = %s AND is_active = TRUE',
            (short_code,)
        )
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        return dict(result) if result else None
    
    def increment_clicks(self, short_code):
        """Increment click count"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        cur.execute(
            'UPDATE urls SET clicks = clicks + 1 WHERE short_code = %s',
            (short_code,)
        )
        conn.commit()
        cur.close()
        conn.close()
    
    def get_stats(self, short_code):
        """Get URL statistics"""
        return self.get_url_by_code(short_code)
