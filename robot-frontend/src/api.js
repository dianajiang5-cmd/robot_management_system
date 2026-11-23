import axios from 'axios';

const api = axios.create({
  // 开发环境直接指向 FastAPI 后端
  baseURL: 'http://127.0.0.1:8000', 
});

// 每次请求自动带上 Token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;