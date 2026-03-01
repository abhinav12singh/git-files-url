Distributed URL Shortener

A production-grade, distributed URL shortener built with Python, Flask, PostgreSQL, and Redis.

Designed for low-latency redirects, collision-resistant hashing, real-time analytics, and scalable deployment using Docker.

🛠 Tech Stack

Backend: Flask (Application Factory Pattern)

Database: PostgreSQL 15

Cache: Redis 7

Containerization: Docker & Docker Compose

Testing: Pytest

✨ Features

⚡ Sub-10ms redirect response with Redis caching

🔒 SHA-256 hashing + Base62 encoding (collision resistant)

📊 Real-time click tracking and analytics

🔄 Cache stampede prevention

🐳 Fully Dockerized multi-container architecture

📈 Designed for horizontal scalability

🛡️ Production-ready configuration

🏗 Architecture
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
        ┌──────┴─────────────┐
        ▼                    ▼
   ┌───────────┐        ┌─────────────┐
   │   Redis   │        │ PostgreSQL  │
   │  (Cache)  │        │  (Storage)  │
   └───────────┘        └─────────────┘
📁 Project Structure
url-shortener/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   └── routes.py
│
├── tests/
│
├── config.py
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
🚀 Quick Start (Docker - Recommended)
1️⃣ Clone Repository
git clone https://github.com/abhinav12singh/git-files-url.git
cd url-shortener
2️⃣ Start Application
docker-compose up --build
3️⃣ Access Application

Since Docker maps:

5001 (host) → 5000 (container)

Open:

http://localhost:5001
⚙️ Docker Setup Details

Flask binds to 0.0.0.0

App container runs on port 5000

Exposed to host via 5001

PostgreSQL runs on internal Docker network

Redis runs on internal Docker network

No volume override in production mode — container holds all project files internally.

🔌 API Documentation
🔹 Shorten URL

POST /shorten

{
  "url": "https://example.com/very/long/url",
  "custom_alias": "my-link",
  "expiration_days": 30
}

Response:

{
  "id": 1,
  "long_url": "https://example.com/very/long/url",
  "short_code": "abc123",
  "short_url": "http://localhost:5001/abc123",
  "click_count": 0
}
🔹 Redirect

GET /<short_code>

Returns 301 redirect to original URL.

🔹 Get Statistics

GET /stats/<short_code>

🔹 Health Check

GET /health

{
  "status": "healthy",
  "service": "url-shortener",
  "version": "1.0.0"
}
🔧 Environment Variables

Create .env file:

Variable	Description
DATABASE_URL	PostgreSQL connection string
REDIS_URL	Redis connection string
REDIS_TTL	Cache TTL
BASE_URL	Base URL for short links
SECRET_KEY	Flask secret key
FLASK_ENV	development / production
LOG_LEVEL	Logging level
📈 Performance Optimizations
Redis Caching

High cache hit rate

TTL-based expiration

Stampede prevention

Collision Prevention

SHA-256 hashing

Base62 encoding

Retry mechanism

Database

Indexed lookups

Optimized query patterns

Connection reuse

🧪 Testing
pytest tests/

With coverage:

pytest --cov=app tests/
🚀 Production Deployment Notes

Before deploying:

Set strong SECRET_KEY

Use secure database credentials

Enable HTTPS

Configure rate limiting

Enable logging aggregation

Use Gunicorn (recommended for production)

Example production command:

gunicorn -w 4 -b 0.0.0.0:5000 run:app
📊 Scaling Strategy
Horizontal Scaling

Multiple Flask containers behind load balancer

Redis cluster

PostgreSQL read replicas

Vertical Scaling

Increase Redis memory

Tune PostgreSQL config

Increase worker processes

🛡 Security Considerations

Prepared statements prevent SQL injection

Environment-based configuration

Internal Docker networking

Optional Redis password protection

🤝 Contributing

Fork the repo

Create branch
git checkout -b feature/feature-name

Commit
git commit -m "Add feature"

Push
git push origin feature/feature-name

Open Pull Request

📜 License

MIT License

👨‍💻 Author

Abhinav Singh

Built with ❤️ using Flask, PostgreSQL, Redis & Docker.
