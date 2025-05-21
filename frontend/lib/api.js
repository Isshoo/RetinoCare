import axios from 'axios';
import { getAccessToken, updateAccessToken, getRefreshToken } from './auth';
import { API_BASE_URL, ENDPOINTS } from './apiConfig';

// Create axios instance with proper CORS configuration
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for CORS with credentials
});

// Add request interceptor to add the auth token to every request
apiClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle token refresh on 401 errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 and we haven't tried to refresh the token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh the token
        const refreshToken = getRefreshToken();
        if (!refreshToken) {
          throw new Error('Refresh token not found');
        }
        
        const response = await axios.post(
          `${API_BASE_URL}${ENDPOINTS.REFRESH}`,
          {},
          {
            headers: {
              'Authorization': `Bearer ${refreshToken}`
            },
            withCredentials: true
          }
        );
        
        const { access_token } = response.data;
        updateAccessToken(access_token);
        
        // Retry the original request with the new token
        originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // If refresh fails, redirect to login or handle as needed
        console.error('Token refresh failed:', refreshError);
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;