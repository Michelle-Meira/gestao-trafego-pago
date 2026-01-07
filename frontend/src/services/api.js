import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: async (email, password) => {
    console.log('🔐 Tentando login:', email);
    
    // CORREÇÃO: Criar URLSearchParams corretamente
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
        },
        body: params.toString(),
      });
      
      console.log('📊 Response status:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json();
        console.error('❌ Login failed:', errorData);
        throw new Error(errorData.detail || 'Login failed');
      }
      
      const data = await response.json();
      console.log('✅ Login successful, token received');
      
      // Salva token
      localStorage.setItem('token', data.access_token);
      
      // Busca perfil do usuário
      const profileResponse = await fetch(`${API_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${data.access_token}`,
          'Accept': 'application/json',
        },
      });
      
      if (profileResponse.ok) {
        const userData = await profileResponse.json();
        localStorage.setItem('user', JSON.stringify(userData));
        console.log('👤 User profile saved:', userData);
      }
      
      return data;
    } catch (error) {
      console.error('💥 Login error:', error);
      throw error;
    }
  },
  
  register: (userData) => 
    api.post('/auth/register', userData),
  
  getProfile: () => api.get('/auth/me'),
  
  changePassword: (data) => api.post('/auth/change-password', data),
};

export const campaignsAPI = {
  getAll: (params) => api.get('/campaigns/', { params }),
  getById: (id) => api.get(`/campaigns/${id}`),
  create: (data) => api.post('/campaigns/', data),
  update: (id, data) => api.put(`/campaigns/${id}`, data),
  delete: (id) => api.delete(`/campaigns/${id}`),
  getMetrics: (id) => api.get(`/campaigns/${id}/metrics`),
  pause: (id) => api.post(`/campaigns/${id}/pause`),
  activate: (id) => api.post(`/campaigns/${id}/activate`),
  getPlatformSummary: (platform) => api.get(`/campaigns/platform/${platform}/summary`),
  populateSample: () => api.post('/campaigns/populate-sample'),
};

export default api;
