/**
 * API Configuration
 * Automatically detects environment and uses appropriate API URL
 */

// Get the API URL based on the environment
export const getApiUrl = (): string => {
  // Check if we're in the browser
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    
    // Production domain
    if (hostname === 'fluxor.pro' || hostname === 'www.fluxor.pro') {
      return 'https://api.fluxor.pro';
    }
    
    // If accessing via IP address (production server)
    if (hostname === '31.97.103.64') {
      return 'http://31.97.103.64:8000';
    }
    
    // Local development on port 5173 (Docker)
    if (hostname === 'localhost' && window.location.port === '5173') {
      return 'http://localhost:8000';
    }
    
    // Local development on port 3000 (Next.js dev server)
    if (hostname === 'localhost' && window.location.port === '3000') {
      return 'http://localhost:8000';
    }
  }
  
  // Default fallback to localhost for SSR
  return 'http://localhost:8000';
};

// Get WebSocket URL based on environment
export const getWsUrl = (): string => {
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    
    // Production domain
    if (hostname === 'fluxor.pro' || hostname === 'www.fluxor.pro') {
      return 'wss://api.fluxor.pro';
    }
    
    // If accessing via IP address (production server)
    if (hostname === '31.97.103.64') {
      return 'ws://31.97.103.64:8000';
    }
    
    // Local development
    if (hostname === 'localhost') {
      return 'ws://localhost:8000';
    }
  }
  
  // Default fallback
  return 'ws://localhost:8000';
};

// Export the API URL as a constant
export const API_URL = getApiUrl();
export const WS_URL = getWsUrl();

// Helper to build full API endpoint
export const apiEndpoint = (path: string): string => {
  const url = getApiUrl();
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${url}${cleanPath}`;
};

// Helper to build full WebSocket endpoint
export const wsEndpoint = (path: string): string => {
  const url = getWsUrl();
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${url}${cleanPath}`;
};

