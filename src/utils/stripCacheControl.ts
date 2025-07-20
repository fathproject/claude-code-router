/**
 * Recursively strips cache_control properties from messages, system prompts, and content
 * This is needed because many LLM providers don't support cache_control properties
 * that are part of Claude's API
 */
export function stripCacheControl(obj: any): any {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(stripCacheControl);
  }

  const cleaned: any = {};
  for (const [key, value] of Object.entries(obj)) {
    if (key === 'cache_control') {
      // Skip cache_control properties entirely
      continue;
    }
    cleaned[key] = stripCacheControl(value);
  }

  return cleaned;
}

/**
 * Strips cache_control properties from a request body containing messages
 */
export function stripCacheControlFromRequest(requestBody: any): any {
  return stripCacheControl(requestBody);
}