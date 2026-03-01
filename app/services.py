import redis
import os
from nanoid import generate as nanoid_generate
from .models import URLModel

class URLShortenerService:
    """Business logic for URL shortening"""
    
    def __init__(self):
        self.url_model = URLModel()
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.cache_ttl = int(os.getenv('REDIS_TTL', 3600))
        
        try:
            self.redis_client = redis.from_url(self.redis_url)
            self.redis_client.ping()
        except Exception as e:
            print(f"Warning: Redis connection failed - {e}")
            self.redis_client = None
    
    def shorten_url(self, original_url, max_retries=5):
        """Create a shortened URL"""
        for attempt in range(max_retries):
            short_code = nanoid_generate(size=7)
            
            # Try to insert into database
            result = self.url_model.create_url(short_code, original_url)
            
            if result:
                # Cache the mapping
                if self.redis_client:
                    try:
                        self.redis_client.setex(
                            short_code, 
                            self.cache_ttl, 
                            original_url
                        )
                    except Exception as e:
                        print(f"Cache error: {e}")
                
                return result
        
        return None
    
    def get_original_url(self, short_code):
        """Get original URL from short code"""
        # Try cache first
        if self.redis_client:
            try:
                cached_url = self.redis_client.get(short_code)
                if cached_url:
                    return cached_url.decode() if isinstance(cached_url, bytes) else cached_url
            except Exception as e:
                print(f"Cache error: {e}")
        
        # Get from database
        url_data = self.url_model.get_url_by_code(short_code)
        
        if url_data:
            # Update cache
            if self.redis_client:
                try:
                    self.redis_client.setex(
                        short_code,
                        self.cache_ttl,
                        url_data['original_url']
                    )
                except Exception as e:
                    print(f"Cache error: {e}")
            
            # Increment clicks
            try:
                self.url_model.increment_clicks(short_code)
            except Exception as e:
                print(f"Database error: {e}")
            
            return url_data['original_url']
        
        return None
    
    def get_stats(self, short_code):
        """Get URL statistics"""
        return self.url_model.get_stats(short_code)
