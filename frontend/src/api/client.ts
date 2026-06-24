import axios from 'axios';

const client = axios.create({
  baseURL: '/api',
  timeout: 30000,
});

client.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error('API error:', err);
    return Promise.reject(err);
  },
);

export default client;
