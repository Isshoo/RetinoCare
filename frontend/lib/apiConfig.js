/**
 * API configuration for the RetinoCare application.
 * Centralizes API URLs and other configuration settings.
 */

// Base API URL with fallback to localhost for development
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

// API endpoints
export const ENDPOINTS = {
  UPLOAD: '/upload',
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  REFRESH: '/auth/refresh',
  DETECTION_HISTORY: '/detection/history',
  PROFILE: '/user/profile',
};

/**
 * Get complete URL for an API endpoint
 * @param {string} endpoint - The endpoint path
 * @returns {string} The complete URL
 */
export const getApiUrl = (endpoint) => `${API_BASE_URL}${endpoint}`;