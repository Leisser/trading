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
    const token = localStorage.getItem('auth_token') || localStorage.getItem('token')
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

// Authentication API methods
export const authAPI = {
  login: async (credentials: { username: string; password: string }) => {
    const response = await api.post('/token/', credentials)
    return response
  },

  logout: async () => {
    const response = await api.post('/logout/')
    return response
  },

  refresh: async (refreshToken: string) => {
    const response = await api.post('/token/refresh/', { refresh: refreshToken })
    return response
  },

  getProfile: async () => {
    const response = await api.get('/profile/')
    return response
  },

  changePassword: async (data: { currentPassword: string; newPassword: string }) => {
    const response = await api.post('/change-password/', data)
    return response
  }
}

// User Management API methods
export const userAPI = {
  getUsers: async (params?: any) => {
    const response = await api.get('/admin/users/', { params })
    return response.data
  },

  getUser: async (id: number) => {
    const response = await api.get(`/admin/users/${id}/`)
    return response.data
  },

  updateUser: async (id: number, data: any) => {
    const response = await api.patch(`/admin/users/${id}/`, data)
    return response.data
  },

  deleteUser: async (id: number) => {
    const response = await api.delete(`/admin/users/${id}/`)
    return response.data
  },

  getUserWallets: async (userId: number) => {
    const response = await api.get(`/admin/users/${userId}/wallets/`)
    return response.data
  },

  getUserTrades: async (userId: number) => {
    const response = await api.get(`/admin/users/${userId}/trades/`)
    return response.data
  }
}

// Wallet Management API methods
export const walletAPI = {
  getWallets: async () => {
    const response = await api.get('/wallets/')
    return response.data
  },

  getWallet: async (id: number) => {
    const response = await api.get(`/wallets/${id}/`)
    return response.data
  },

  getDepositRequests: async (status?: string) => {
    const params = status ? { status } : {}
    const response = await api.get('/api/admin/deposits/', { params })
    return response.data
  },

  approveDeposit: async (id: number, data: any = {}) => {
    const response = await api.post(`/api/admin/deposits/${id}/approve/`, { action: 'approve', ...data })
    return response.data
  },

  rejectDeposit: async (id: number, reason: string = '') => {
    const response = await api.post(`/api/admin/deposits/${id}/approve/`, { action: 'reject', admin_notes: reason })
    return response.data
  },

  getWithdrawRequests: async (status?: string) => {
    const params = status ? { status } : {}
    const response = await api.get('/api/admin/withdrawals/', { params })
    return response.data
  },

  approveWithdrawal: async (id: number, data: any = {}) => {
    const response = await api.post(`/api/admin/withdrawals/${id}/approve/`, { action: 'approve', ...data })
    return response.data
  },

  rejectWithdrawal: async (id: number, reason: string = '') => {
    const response = await api.post(`/api/admin/withdrawals/${id}/approve/`, { action: 'reject', admin_notes: reason })
    return response.data
  },

  getDepositWallets: async () => {
    const response = await api.get('/trades/deposit-wallets/')
    return response.data
  },

  createDepositWallet: async (data: any) => {
    const response = await api.post('/trades/deposit-wallets/', data)
    return response.data
  },

  updateDepositWallet: async (id: number, data: any) => {
    const response = await api.patch(`/trades/deposit-wallets/${id}/`, data)
    return response.data
  }
}

// Trading Management API methods
export const tradingAPI = {
  getTrades: async (params?: any) => {
    const response = await api.get('/trades/', { params })
    return response.data
  },

  getTrade: async (id: number) => {
    const response = await api.get(`/trades/${id}/`)
    return response.data
  },

  getOrders: async (params?: any) => {
    const response = await api.get('/trading/orders/', { params })
    return response.data
  },

  cancelOrder: async (id: number) => {
    const response = await api.post(`/trading/orders/${id}/cancel/`)
    return response.data
  },

  getTradingPairs: async () => {
    const response = await api.get('/market/trading-pairs/')
    return response.data
  },

  updateTradingPair: async (id: number, data: any) => {
    const response = await api.patch(`/market/trading-pairs/${id}/`, data)
    return response.data
  },

  enableTrading: async (pairId: number) => {
    const response = await api.post(`/market/trading-pairs/${pairId}/enable/`)
    return response.data
  },

  disableTrading: async (pairId: number) => {
    const response = await api.post(`/market/trading-pairs/${pairId}/disable/`)
    return response.data
  }
}

// Create a combined API object
const combinedAPI = {
  auth: authAPI,
  users: userAPI,
  wallets: walletAPI,
  trading: tradingAPI,
  dashboard: dashboardAPI
}

export default combinedAPI
