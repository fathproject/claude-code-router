# Ethical Web Scraper Plugin

This plugin provides educational web scraping capabilities with built-in ethical constraints and security measures. It's designed for learning purposes and demonstrates responsible scraping practices.

## ⚠️ Important Notice

This scraper is for **educational purposes only**. It includes:
- Mock data generation instead of actual scraping
- Rate limiting and request throttling
- Robots.txt compliance checking
- Security measures to prevent abuse

**Do NOT use this for actual scraping of booking.com or other commercial websites without proper authorization.**

## Features

### 🔒 Security Measures
- API key authentication required
- Rate limiting (configurable, default: 5 requests/minute)
- Concurrent request limiting (default: 1 concurrent request)
- IP-based tracking and throttling
- Request logging and monitoring

### 🤖 Ethical Constraints
- Robots.txt compliance checking
- Configurable delays between requests (default: 3 seconds)
- Respectful user agent identification
- Educational mock data instead of real scraping
- Built-in safeguards against commercial site scraping

### 📚 Educational Value
- Demonstrates proper scraping architecture
- Shows rate limiting implementation
- Teaches robots.txt respect
- Explains security considerations
- Provides real-world patterns and practices

## Configuration

Add these settings to your `~/.claude-code-router/config.json`:

```json
{
  "ENABLE_SCRAPER": false,
  "SCRAPER_RATE_LIMIT": 5,
  "APIKEY": "your-secret-key"
}
```

### Configuration Options

- `ENABLE_SCRAPER`: Enable/disable the scraper (default: false)
- `SCRAPER_RATE_LIMIT`: Maximum requests per minute (default: 5)
- `APIKEY`: Required for authentication

## API Endpoints

### GET /scraper/help
Get documentation and ethical guidelines.

**Response:**
```json
{
  "name": "Educational Web Scraper",
  "endpoints": {...},
  "ethical_guidelines": [...],
  "example_request": {...}
}
```

### POST /scraper/educational
Simulate educational scraping with mock data.

**Request:**
```json
{
  "url": "https://example.com/hotels"
}
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer your-api-key
```

**Response:**
```json
{
  "success": true,
  "url": "https://example.com/hotels",
  "timestamp": "2023-12-01T10:00:00.000Z",
  "data": {
    "type": "hotel_search_results",
    "results": [...],
    "educational_notice": "Real hotel data should only be accessed through official APIs"
  },
  "educational": true,
  "note": "This is mock data for educational purposes."
}
```

### GET /scraper/stats
View scraper statistics and configuration (requires authentication).

**Response:**
```json
{
  "activeConnections": [...],
  "rateLimitEntries": 0,
  "robotsTxtCacheSize": 0,
  "config": {
    "enabled": false,
    "maxRequests": 5,
    "windowMs": 60000,
    "minDelay": 3000,
    "maxConcurrent": 1
  }
}
```

## Usage Examples

### Enable the Scraper

1. Set `ENABLE_SCRAPER: true` in your config
2. Ensure `APIKEY` is configured
3. Restart the claude-code-router service

### Test Educational Scraping

```bash
# Start the service
ccr start

# Test the educational endpoint
curl -X POST http://localhost:3456/scraper/educational \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"url": "https://example.com/hotels"}'
```

### View Help and Guidelines

```bash
curl http://localhost:3456/scraper/help
```

### Check Scraper Statistics

```bash
curl -H "Authorization: Bearer your-api-key" \
  http://localhost:3456/scraper/stats
```

## Rate Limiting

The scraper implements multiple layers of rate limiting:

1. **Request Rate Limiting**: Maximum 5 requests per minute per IP (configurable)
2. **Concurrent Request Limiting**: Maximum 1 concurrent request per IP
3. **Delay Enforcement**: Minimum 3 seconds between requests
4. **Automatic Cleanup**: Rate limit windows reset automatically

## Robots.txt Compliance

The scraper automatically:
- Checks robots.txt for each domain
- Caches robots.txt responses (1 hour TTL)
- Blocks requests to disallowed paths
- Specifically prevents scraping of booking.com for safety

## Error Handling

Common error responses:

```json
// Rate limit exceeded
{
  "error": "Rate limit exceeded. Please wait before making more requests."
}

// Scraper disabled
{
  "error": "Scraper is disabled. Enable in configuration for educational use only."
}

// Robots.txt blocked
{
  "error": "Scraping not allowed by robots.txt or site policy."
}

// Invalid URL
{
  "error": "Invalid URL format"
}
```

## Ethical Guidelines

When using this educational scraper:

1. **Always respect robots.txt** - The scraper checks this automatically
2. **Use appropriate delays** - Built-in 3-second minimum delays
3. **Monitor your requests** - Check stats endpoint regularly
4. **Respect rate limits** - Don't try to bypass the built-in limits
5. **Use official APIs when available** - This is just for learning
6. **Never scrape without permission** - Always check terms of service

## Security Features

- **Authentication Required**: All endpoints require valid API key
- **IP Tracking**: Rate limits are applied per IP address
- **Request Logging**: All scraper requests are logged
- **Abuse Prevention**: Multiple layers of protection against misuse
- **Graceful Degradation**: Safe fallbacks for all error conditions

## Legal and Ethical Considerations

This tool is provided for educational purposes only. Users must:

- Obtain proper authorization before scraping any website
- Respect website terms of service
- Follow applicable laws and regulations
- Use official APIs whenever possible
- Consider the impact on website performance
- Respect intellectual property rights

## Troubleshooting

### Scraper Not Working
1. Check that `ENABLE_SCRAPER: true` in config
2. Verify `APIKEY` is set and correct
3. Ensure service is running: `ccr status`
4. Check logs for error messages

### Rate Limit Issues
1. Wait for rate limit window to reset (1 minute)
2. Reduce request frequency
3. Check current limits with `/scraper/stats`

### Authentication Errors
1. Verify API key in config matches request header
2. Use `Authorization: Bearer <key>` or `x-api-key: <key>` header
3. Ensure key is properly configured in `~/.claude-code-router/config.json`

## Contributing

This educational scraper demonstrates many important concepts:
- Rate limiting implementation
- Middleware design patterns
- Security best practices
- Ethical web scraping principles
- Error handling and logging

Feel free to study the code and adapt the patterns for your own educational projects.