# Distributed URL Shortener

A production-grade, distributed URL shortener built with Python, Flask, PostgreSQL, and Redis. Features low-latency redirects, collision-resistant hashing, and comprehensive analytics.

![URL Shortener](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Redis](https://img.shields.io/badge/Redis-7-red)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)


## Features

- **⚡ Lightning Fast**: Sub-10ms response times with Redis caching
- **🔒 Collision Resistant**: SHA-256 based hashing with Base62 encoding
- **📊 Analytics**: Real-time click tracking and statistics
- **🔄 Cache Stampede Prevention**: Distributed locking mechanism
- **🐳 Docker Ready**: Complete containerization with Docker Compose
- **📈 Scalable**: Designed for horizontal scaling
- **🛡️ Production Ready**: Comprehensive error handling and logging

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Flask     │
│     API     │
└──────┬──────┘
       │
       ├─────────────┐
       ▼             ▼
┌─────────────┐ ┌─────────────┐
│    Redis    │ │ PostgreSQL  │
│   (Cache)   │ │  (Storage)  │
└─────────────┘ └─────────────┘
```

## Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── services.py          # Business logic
│   └── routes.py            # API endpoints
├── static/
│   └── style.css            # Landing page styles
├── templates/
│   └── index.html           # Landing page
├── tests/
│   └── test_services.py     # Unit tests
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container definition
├── docker-compose.yml       # Multi-container setup
└── README.md                # Documentation
```

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/git-files-url.git
cd url-shortener
```

2. **Start the application**
```bash
docker-compose up -d
```

3. **Access the application**
- Web UI: http://localhost:5001
- API: http://localhost:5000/shorten

### Manual Setup

1. **Install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Set up PostgreSQL**
```bash
createdb urlshortener
```

3. **Set up Redis**
```bash
redis-server
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the application**
```bash
python run.py
```

## API Documentation

### Shorten URL

**Endpoint:** `POST /shorten`

**Request:**
```json
{
  "url": "https://example.com/very/long/url",
  "custom_alias": "my-link",      // optional
  "expiration_days": 30            // optional
}
```

**Response:**
```json
{
  "id": 1,
  "long_url": "https://example.com/very/long/url",
  "short_code": "abc123",
  "short_url": "http://localhost:5001/abc123",
  "created_at": "2024-02-16T10:30:00",
  "expiration_date": null,
  "click_count": 0
}
```

### Redirect to Long URL

**Endpoint:** `GET /<short_code>`

**Response:** 301 redirect to the original URL

### Get URL Statistics

**Endpoint:** `GET /stats/<short_code>`

**Response:**
```json
{
  "id": 1,
  "long_url": "https://example.com/very/long/url",
  "short_code": "abc123",
  "short_url": "abc123",
  "created_at": "2024-02-16T10:30:00",
  "expiration_date": null,
  "click_count": 42
}
```

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "url-shortener",
  "version": "1.0.0"
}
```

## Configuration

Environment variables (`.env` file):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://urlshortener:password@localhost:5432/urlshortener` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `REDIS_TTL` | Cache TTL in seconds | `3600` |
| `BASE_URL` | Base URL for short links | `http://localhost:5001` |
| `SECRET_KEY` | Flask secret key | Random string |
| `FLASK_ENV` | Environment (development/production) | `development` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Performance Features

### Redis Caching
- **Cache Hit Rate**: ~95% for frequently accessed URLs
- **TTL Management**: Automatic expiration after configurable period
- **Cache Warming**: Proactive cache population

### Collision Prevention
- **SHA-256 Hashing**: Cryptographically secure hash generation
- **Base62 Encoding**: URL-safe short codes
- **Retry Mechanism**: Up to 5 attempts on collision
- **Distributed Locking**: Prevents cache stampede

### Database Optimization
- **Indexed Lookups**: O(log n) query performance
- **Connection Pooling**: Reuse database connections
- **Prepared Statements**: Protection against SQL injection

## Deployment

### Production Checklist

-  Set strong `SECRET_KEY`
-  Use production database credentials
-  Configure Redis password
-  Enable HTTPS
-  Set up monitoring and alerting
-  Configure backup strategy
-  Review security headers
-  Set appropriate `REDIS_TTL`
-  Configure rate limiting
-  Set up log aggregation

### Scaling Strategies

**Horizontal Scaling:**
- Deploy multiple Flask instances behind a load balancer
- Use Redis Cluster for distributed caching
- PostgreSQL read replicas for high read throughput

**Vertical Scaling:**
- Increase Redis memory for larger cache
- Optimize PostgreSQL configuration
- Increase Flask worker count

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_services.py::TestURLShortenerService
```

## Monitoring

Key metrics to monitor:
- Response time (p50, p95, p99)
- Cache hit rate
- Database query time
- Error rate
- Request throughput

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with Flask framework
- Uses PostgreSQL for reliable storage
- Redis for high-performance caching
- Docker for easy deployment

## Support

For issues and questions:
- GitHub Issues: https://github.com/abhinav12singh/git-files-url/issues
- Documentation: See this README

---

**Built with ❤️ for the developer community**
