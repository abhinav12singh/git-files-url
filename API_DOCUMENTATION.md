# API Documentation

Complete API reference for the Distributed URL Shortener.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. Consider adding API keys or OAuth for production use.

## Response Format

All responses are in JSON format with appropriate HTTP status codes.

### Success Response Structure

```json
{
  "id": 1,
  "long_url": "string",
  "short_code": "string",
  "short_url": "string",
  "created_at": "ISO 8601 datetime",
  "expiration_date": "ISO 8601 datetime | null",
  "click_count": 0
}
```

### Error Response Structure

```json
{
  "error": "Error message description"
}
```

## Endpoints

### Health Check

Check if the service is healthy and running.

**Endpoint:** `GET /health`

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "service": "url-shortener",
  "version": "1.0.0"
}
```

**Example:**

```bash
curl http://localhost:5000/health
```

---

### Shorten URL

Create a shortened URL from a long URL.

**Endpoint:** `POST /shorten`

**Headers:**
- `Content-Type: application/json`

**Request Body:**

```json
{
  "url": "string (required)",
  "custom_alias": "string (optional)",
  "expiration_days": "integer (optional, 1-365)"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | The long URL to shorten. Must be a valid URL. |
| `custom_alias` | string | No | Custom short code (3-20 chars, alphanumeric + hyphens). |
| `expiration_days` | integer | No | Days until URL expires (1-365). Default: never expires. |

**Response:** `201 Created`

```json
{
  "id": 123,
  "long_url": "https://example.com/very/long/url/path",
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123",
  "created_at": "2024-02-16T10:30:00.000000",
  "expiration_date": null,
  "click_count": 0
}
```

**Error Responses:**

| Status Code | Description |
|-------------|-------------|
| `400 Bad Request` | Invalid URL format, missing URL, or custom alias already exists |
| `500 Internal Server Error` | Server error during URL creation |

**Examples:**

**Basic URL Shortening:**

```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/very/long/url"
  }'
```

**With Custom Alias:**

```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/my-page",
    "custom_alias": "my-link"
  }'
```

**With Expiration:**

```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/temporary-page",
    "expiration_days": 7
  }'
```

**With All Options:**

```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/campaign",
    "custom_alias": "winter-sale",
    "expiration_days": 30
  }'
```

---

### Redirect to Long URL

Redirect from a short code to the original long URL.

**Endpoint:** `GET /<short_code>`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `short_code` | string | Yes | The short code to redirect from |

**Response:** `301 Moved Permanently`

Redirects to the original long URL.

**Error Responses:**

| Status Code | Description |
|-------------|-------------|
| `404 Not Found` | Short code doesn't exist or has expired |
| `500 Internal Server Error` | Server error during retrieval |

**Example:**

```bash
# This will redirect to the long URL
curl -L http://localhost:5000/abc123

# Without following redirects (to see the 301 response)
curl -I http://localhost:5000/abc123
```

**Response Headers:**

```
HTTP/1.1 301 MOVED PERMANENTLY
Location: https://example.com/very/long/url
```

---

### Get URL Statistics

Retrieve statistics and information about a shortened URL.

**Endpoint:** `GET /stats/<short_code>`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `short_code` | string | Yes | The short code to get stats for |

**Response:** `200 OK`

```json
{
  "id": 123,
  "long_url": "https://example.com/very/long/url",
  "short_code": "abc123",
  "short_url": "abc123",
  "created_at": "2024-02-16T10:30:00.000000",
  "expiration_date": "2024-03-16T10:30:00.000000",
  "click_count": 42
}
```

**Error Responses:**

| Status Code | Description |
|-------------|-------------|
| `404 Not Found` | Short code doesn't exist |
| `500 Internal Server Error` | Server error during retrieval |

**Example:**

```bash
curl http://localhost:5000/stats/abc123
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider implementing:

- Per-IP rate limiting (e.g., 100 requests/hour)
- Per-endpoint rate limiting
- API key-based quotas

## Error Codes

| HTTP Status | Meaning |
|-------------|---------|
| `200 OK` | Request successful |
| `201 Created` | Resource created successfully |
| `301 Moved Permanently` | URL redirect |
| `400 Bad Request` | Invalid request parameters |
| `404 Not Found` | Resource not found |
| `500 Internal Server Error` | Server error |

## Common Error Messages

### URL Validation Errors

```json
{
  "error": "URL cannot be empty"
}
```

```json
{
  "error": "Invalid URL format"
}
```

```json
{
  "error": "URL exceeds maximum length of 2048"
}
```

### Custom Alias Errors

```json
{
  "error": "Custom alias already exists"
}
```

```json
{
  "error": "Alias must be between 3 and 20 characters"
}
```

```json
{
  "error": "Alias can only contain letters, numbers, and hyphens"
}
```

### Expiration Errors

```json
{
  "error": "Expiration days must be between 1 and 365"
}
```

### Not Found Errors

```json
{
  "error": "Short URL not found"
}
```

```json
{
  "error": "Short URL has expired"
}
```

## Usage Examples

### Python

```python
import requests

# Shorten URL
response = requests.post(
    'http://localhost:5000/shorten',
    json={
        'url': 'https://example.com/long/url',
        'custom_alias': 'my-link',
        'expiration_days': 30
    }
)
data = response.json()
short_url = data['short_url']

# Get statistics
stats = requests.get(f'http://localhost:5000/stats/{data["short_code"]}').json()
print(f"Clicks: {stats['click_count']}")

# Follow redirect
original_url = requests.get(short_url, allow_redirects=True).url
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

// Shorten URL
async function shortenUrl(longUrl) {
  const response = await axios.post('http://localhost:5000/shorten', {
    url: longUrl,
    custom_alias: 'my-link',
    expiration_days: 30
  });
  return response.data;
}

// Get statistics
async function getStats(shortCode) {
  const response = await axios.get(`http://localhost:5000/stats/${shortCode}`);
  return response.data;
}

// Usage
shortenUrl('https://example.com/long/url')
  .then(data => {
    console.log('Short URL:', data.short_url);
    return getStats(data.short_code);
  })
  .then(stats => {
    console.log('Click count:', stats.click_count);
  });
```

### JavaScript (Browser)

```javascript
// Shorten URL
async function shortenUrl(longUrl) {
  const response = await fetch('http://localhost:5000/shorten', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      url: longUrl
    })
  });
  return await response.json();
}

// Get statistics
async function getStats(shortCode) {
  const response = await fetch(`http://localhost:5000/stats/${shortCode}`);
  return await response.json();
}

// Usage
shortenUrl('https://example.com/long/url')
  .then(data => {
    console.log('Short URL:', data.short_url);
    document.getElementById('result').textContent = data.short_url;
  });
```

### cURL

```bash
# Shorten URL
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/long/url"}'

# Get statistics
curl http://localhost:5000/stats/abc123

# Follow redirect
curl -L http://localhost:5000/abc123

# Health check
curl http://localhost:5000/health
```

## Best Practices

### URL Validation

Always validate URLs on the client side before sending to the API:

```javascript
function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}
```

### Error Handling

Always handle errors appropriately:

```python
try:
    response = requests.post('http://localhost:5000/shorten', json={'url': url})
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

### Custom Aliases

Use descriptive custom aliases:
- ✅ Good: `winter-sale-2024`, `product-launch`, `blog-post-ai`
- ❌ Bad: `a`, `xx`, `123`

### Expiration

Set appropriate expiration for temporary links:
- Campaign links: 30-90 days
- Event links: Duration of event + 7 days
- Permanent content: No expiration

## Performance Considerations

### Caching

The API uses Redis caching for frequently accessed URLs:
- Cache TTL: 1 hour (configurable via `REDIS_TTL`)
- Cache invalidation on URL expiration
- Distributed locking to prevent cache stampede

### Response Times

Typical response times:
- Cache hit: < 10ms
- Cache miss: < 50ms
- URL creation: < 100ms

### Scalability

For high-traffic scenarios:
- Deploy multiple API instances behind a load balancer
- Use Redis Cluster for distributed caching
- Implement connection pooling for PostgreSQL

## Future API Enhancements

Planned features:
- [ ] API authentication (API keys)
- [ ] Bulk URL shortening
- [ ] URL analytics (detailed click tracking)
- [ ] QR code generation
- [ ] Custom domains
- [ ] URL preview endpoint
- [ ] Batch operations
- [ ] Webhook notifications
- [ ] Rate limiting

## Support

For API support:
- GitHub Issues: https://github.com/yourusername/url-shortener/issues
- Documentation: See README.md

---

**API Version:** 1.0.0  
**Last Updated:** February 2024
