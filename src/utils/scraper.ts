import { FastifyRequest, FastifyReply } from "fastify";
import { log } from "./log";

// Rate limiting configuration
interface RateLimit {
  requests: number;
  windowMs: number;
  lastReset: number;
}

// Scraper configuration interface
interface ScraperConfig {
  enableScraper?: boolean;
  rateLimit?: {
    maxRequests: number;
    windowMs: number;
  };
  userAgent?: string;
  respectRobotsTxt?: boolean;
  minDelay?: number;
  maxConcurrentRequests?: number;
}

// In-memory rate limiting store (in production, use Redis or similar)
const rateLimitStore = new Map<string, RateLimit>();

// Track active requests per IP
const activeRequests = new Map<string, number>();

/**
 * Ethical web scraper utility with built-in rate limiting and security measures
 * This is for educational purposes and demonstrates responsible scraping practices
 */
export class EthicalScraper {
  private config: ScraperConfig;
  private robotsTxtCache = new Map<string, { allowed: boolean; timestamp: number }>();

  constructor(config: ScraperConfig = {}) {
    this.config = {
      enableScraper: false,
      rateLimit: {
        maxRequests: 10,
        windowMs: 60000, // 1 minute
      },
      userAgent: "EthicalScraper/1.0 (+https://github.com/educational-scraper)",
      respectRobotsTxt: true,
      minDelay: 2000, // 2 seconds between requests
      maxConcurrentRequests: 2,
      ...config,
    };
  }

  /**
   * Check if scraping is allowed for a specific URL based on robots.txt
   */
  private async checkRobotsTxt(url: string): Promise<boolean> {
    if (!this.config.respectRobotsTxt) return true;

    try {
      const urlObj = new URL(url);
      const robotsUrl = `${urlObj.protocol}//${urlObj.host}/robots.txt`;
      const cacheKey = robotsUrl;
      
      // Check cache (valid for 1 hour)
      const cached = this.robotsTxtCache.get(cacheKey);
      if (cached && Date.now() - cached.timestamp < 3600000) {
        return cached.allowed;
      }

      // This is a simplified robots.txt check
      // In a real implementation, you would fetch and parse robots.txt
      log(`Checking robots.txt for ${robotsUrl}`);
      
      // For educational purposes, we'll assume scraping is NOT allowed for booking.com
      const isBookingCom = url.includes('booking.com');
      const allowed = !isBookingCom; // Prevent actual scraping of booking.com
      
      this.robotsTxtCache.set(cacheKey, { allowed, timestamp: Date.now() });
      return allowed;
    } catch (error) {
      log(`Error checking robots.txt: ${error}`);
      return false; // Default to not allowed on error
    }
  }

  /**
   * Rate limiting check
   */
  private checkRateLimit(clientId: string): boolean {
    const now = Date.now();
    const limit = rateLimitStore.get(clientId);

    if (!limit) {
      rateLimitStore.set(clientId, {
        requests: 1,
        windowMs: this.config.rateLimit!.windowMs,
        lastReset: now,
      });
      return true;
    }

    // Reset window if expired
    if (now - limit.lastReset > limit.windowMs) {
      limit.requests = 1;
      limit.lastReset = now;
      return true;
    }

    // Check if under limit
    if (limit.requests < this.config.rateLimit!.maxRequests) {
      limit.requests++;
      return true;
    }

    return false;
  }

  /**
   * Check concurrent request limits
   */
  private checkConcurrentLimit(clientId: string): boolean {
    const active = activeRequests.get(clientId) || 0;
    return active < this.config.maxConcurrentRequests!;
  }

  /**
   * Simulate a scraping request with educational content
   */
  async scrapeEducational(url: string, clientId: string): Promise<any> {
    // Security checks
    if (!this.config.enableScraper) {
      throw new Error("Scraper is disabled. Enable in configuration for educational use only.");
    }

    if (!this.checkRateLimit(clientId)) {
      throw new Error("Rate limit exceeded. Please wait before making more requests.");
    }

    if (!this.checkConcurrentLimit(clientId)) {
      throw new Error("Too many concurrent requests. Please wait for previous requests to complete.");
    }

    if (!(await this.checkRobotsTxt(url))) {
      throw new Error("Scraping not allowed by robots.txt or site policy. This is for educational purposes only.");
    }

    // Track active request
    const currentActive = activeRequests.get(clientId) || 0;
    activeRequests.set(clientId, currentActive + 1);

    try {
      // Simulate delay (respectful crawling)
      await new Promise(resolve => setTimeout(resolve, this.config.minDelay));

      log(`Educational scraper simulating request to: ${url}`);

      // Instead of actual scraping, return educational mock data
      const mockData = this.generateEducationalMockData(url);
      
      return {
        success: true,
        url,
        timestamp: new Date().toISOString(),
        data: mockData,
        educational: true,
        note: "This is mock data for educational purposes. Actual scraping requires proper authorization and respect for terms of service.",
      };
    } finally {
      // Release concurrent request slot
      const active = activeRequests.get(clientId) || 1;
      if (active <= 1) {
        activeRequests.delete(clientId);
      } else {
        activeRequests.set(clientId, active - 1);
      }
    }
  }

  /**
   * Generate educational mock data instead of real scraping
   */
  private generateEducationalMockData(url: string): any {
    if (url.includes('booking.com') || url.includes('hotels')) {
      return {
        type: "hotel_search_results",
        results: [
          {
            name: "Example Hotel for Education",
            location: "Educational City",
            price: "$100/night",
            rating: 4.5,
            availability: true,
            note: "This is fictional data for educational purposes only"
          },
          {
            name: "Learning Lodge",
            location: "Study Town",
            price: "$85/night",
            rating: 4.2,
            availability: true,
            note: "This demonstrates data structure only"
          }
        ],
        educational_notice: "Real hotel data should only be accessed through official APIs with proper authorization"
      };
    }

    return {
      type: "generic_page_content",
      title: "Educational Scraping Example",
      content: "This represents structured data that could be extracted from a webpage",
      educational_notice: "Always respect robots.txt, terms of service, and rate limits when scraping"
    };
  }

  /**
   * Get scraper statistics
   */
  getStats(): any {
    return {
      activeConnections: Array.from(activeRequests.entries()),
      rateLimitEntries: rateLimitStore.size,
      robotsTxtCacheSize: this.robotsTxtCache.size,
      config: {
        enabled: this.config.enableScraper,
        maxRequests: this.config.rateLimit?.maxRequests,
        windowMs: this.config.rateLimit?.windowMs,
        minDelay: this.config.minDelay,
        maxConcurrent: this.config.maxConcurrentRequests,
      }
    };
  }
}

/**
 * Middleware for handling scraper requests
 */
export const scraperMiddleware = (scraperConfig: ScraperConfig = {}) => {
  const scraper = new EthicalScraper(scraperConfig);

  return async (req: FastifyRequest, reply: FastifyReply) => {
    // Only handle scraper-specific routes
    if (!req.url.startsWith('/scraper/')) {
      return;
    }

    const clientId = req.ip || 'unknown';

    try {
      if (req.url === '/scraper/stats' && req.method === 'GET') {
        const stats = scraper.getStats();
        reply.send(stats);
        return;
      }

      if (req.url === '/scraper/educational' && req.method === 'POST') {
        const body = req.body as any;
        const url = body?.url;

        if (!url) {
          reply.status(400).send({ error: "URL is required" });
          return;
        }

        // Validate URL format
        try {
          new URL(url);
        } catch {
          reply.status(400).send({ error: "Invalid URL format" });
          return;
        }

        const result = await scraper.scrapeEducational(url, clientId);
        reply.send(result);
        return;
      }

      if (req.url === '/scraper/help' && req.method === 'GET') {
        reply.send({
          name: "Educational Web Scraper",
          version: "1.0.0",
          endpoints: {
            "POST /scraper/educational": "Simulate educational scraping with rate limits",
            "GET /scraper/stats": "Get scraper statistics and configuration",
            "GET /scraper/help": "This help message"
          },
          ethical_guidelines: [
            "Always respect robots.txt",
            "Implement proper rate limiting",
            "Use appropriate delays between requests",
            "Respect website terms of service",
            "Consider official APIs instead of scraping",
            "This tool is for educational purposes only"
          ],
          example_request: {
            url: "POST /scraper/educational",
            body: { url: "https://example.com/hotels" },
            headers: { "Content-Type": "application/json" }
          }
        });
        return;
      }

      reply.status(404).send({ error: "Scraper endpoint not found" });
    } catch (error) {
      log(`Scraper error: ${error}`);
      reply.status(500).send({ 
        error: error instanceof Error ? error.message : "Internal scraper error",
        educational: true 
      });
    }
  };
};