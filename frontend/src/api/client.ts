import axios from 'axios';

const client = axios.create({
  baseURL: '/api',
  timeout: 30000,
});

// Auth token interceptor — reads from sessionStorage on every request
client.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('xczs_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      sessionStorage.removeItem('xczs_token');
      window.location.href = '/login';
    }
    console.error('API error:', err);
    return Promise.reject(err);
  },
);

export default client;
