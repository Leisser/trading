import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired, redirect to login
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Dashboard API methods
export const dashboardAPI = {
  // Get dashboard statistics
  getStats: async () => {
    const response = await api.get('/dashboard/stats/')
    return response.data
  },

  // Get trading data
  getTradingData: async () => {
    const response = await api.get('/trading/stats/')
    return response.data
  },

  // Get market data
  getMarketData: async () => {
    const response = await api.get('/market/prices/')
    return response.data
  },

  // Get user statistics
  getUserStats: async () => {
    const response = await api.get('/accounts/user-stats/')
    return response.data
  },

  // Get recent trades
  getRecentTrades: async (limit = 10) => {
    const response = await api.get(`/trades/recent/?limit=${limit}`)
    return response.data
  },

  // Get system health
  getSystemHealth: async () => {
    const response = await api.get('/api/health/')
    return response.data
  },

  // Get cryptocurrency data
  getCryptocurrencies: async () => {
    const response = await api.get('/market/cryptocurrencies/')
    return response.data
  },

  // Get portfolio data
  getPortfolioData: async () => {
    const response = await api.get('/trading/portfolio/')
    return response.data
  },

  // Get risk metrics
  getRiskMetrics: async () => {
    const response = await api.get('/risk/metrics/')
    return response.data
  },

  // Get compliance data
  getComplianceData: async () => {
    const response = await api.get('/compliance/status/')
    return response.data
  },

  // Get blockchain data
  getBlockchainData: async () => {
    const response = await api.get('/blockchain/stats/')
    return response.data
  },

  // Get wallet data
  getWalletData: async () => {
    const response = await api.get('/wallets/balance/')
    return response.data
  }
}

export default api
