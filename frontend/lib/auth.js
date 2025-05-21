// lib/auth.js

const isBrowser = typeof window !== 'undefined';

/**
 * Store authentication tokens in localStorage
 * @param {string} accessToken - JWT access token
 * @param {string} refreshToken - JWT refresh token for token renewal
 */
export const setTokens = ({ access_token, refresh_token, user }) => {
  if (!isBrowser) return;
  
  localStorage.setItem("accessToken", access_token);
  localStorage.setItem("refreshToken", refresh_token);
  if (user) {
    localStorage.setItem("user", JSON.stringify(user));
  }
};

/**
 * Get the access token from localStorage
 * @returns {string|null} The stored access token or null
 */
export const getAccessToken = () => {
  if (!isBrowser) return null;
  return localStorage.getItem("accessToken");
};

/**
 * Get the refresh token from localStorage
 * @returns {string|null} The stored refresh token or null
 */
export const getRefreshToken = () => {
  if (!isBrowser) return null;
  return localStorage.getItem("refreshToken");
};

/**
 * Get the current user data from localStorage
 * @returns {Object|null} The user data or null
 */
export const getUser = () => {
  if (!isBrowser) return null;
  const userData = localStorage.getItem("user");
  return userData ? JSON.parse(userData) : null;
};

/**
 * Remove all authentication data from localStorage
 */
export const clearAuth = () => {
  if (!isBrowser) return;
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("user");
};

/**
 * Check if the user is authenticated
 * @returns {boolean} True if authenticated, false otherwise
 */
export const isAuthenticated = () => {
  if (!isBrowser) return false;
  return !!getAccessToken();
};

/**
 * Store only the access token (used during token refresh)
 * @param {string} accessToken - New JWT access token
 */
export const updateAccessToken = (accessToken) => {
  if (!isBrowser) return;
  localStorage.setItem("accessToken", accessToken);
};

// For backward compatibility
export const setToken = (token) => {
  if (!isBrowser) return;
  localStorage.setItem("accessToken", token);
};

export const getToken = getAccessToken;
export const removeToken = clearAuth;