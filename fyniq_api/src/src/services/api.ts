import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { useNotifications } from '@/utils/notifications'
import { useAuthStore } from '@/stores/auth'

// Create axios instance
const apiService: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor
apiService.interceptors.request.use(
  (config) => {
    // Add timestamp to prevent caching
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    
    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`🚀 ${config.method?.toUpperCase()} ${config.url}`, {
        params: config.params,
        data: config.data
      })
    }
    
    return config
  },
  (error) => {
    console.error('Request interceptor error:', error)
    return Promise.reject(error)
  }
)

// Add auth token to requests
apiService.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    
    // Add timestamp to prevent caching for GET requests
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    
    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`🚀 ${config.method?.toUpperCase()} ${config.url}`, {
        params: config.params,
        data: config.data
      })
    }
    
    return config
  },
  (error) => {
    console.error('Request interceptor error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
apiService.interceptors.response.use(
  (response: AxiosResponse) => {
    // Log response in development
    if (import.meta.env.DEV) {
      console.log(`✅ ${response.config.method?.toUpperCase()} ${response.config.url}`, {
        status: response.status,
        data: response.data
      })
    }
    
    return response
  },
  (error: AxiosError) => {
    const { showNotification } = useNotifications()
    
    // Log error in development
    if (import.meta.env.DEV) {
      console.error(`❌ ${error.config?.method?.toUpperCase()} ${error.config?.url}`, {
        status: error.response?.status,
        data: error.response?.data
      })
    }
    
    // Handle network errors
    if (!error.response) {
      showNotification({
        type: 'error',
        title: 'Network Error',
        message: 'Please check your connection and try again.'
      })
      return Promise.reject(error)
    }
    
    // Handle specific error codes
    const status = error.response.status
    const data = error.response.data as any
    
    switch (status) {
      case 400:
        // Bad request - usually validation errors
        if (data?.detail) {
          showNotification({
            type: 'error',
            title: 'Validation Error',
            message: data.detail
          })
        }
        break
        
      case 401:
        // Unauthorized - redirect to login
        const authStore = useAuthStore()
        authStore.logout()
        break
        
      case 403:
        // Forbidden
        showNotification({
          type: 'error',
          title: 'Access Denied',
          message: 'You do not have permission to perform this action.'
        })
        break
        
      case 404:
        // Not found
        showNotification({
          type: 'error',
          title: 'Not Found',
          message: 'The requested resource was not found.'
        })
        break
        
      case 429:
        // Rate limited
        showNotification({
          type: 'warning',
          title: 'Rate Limited',
          message: 'Too many requests. Please wait a moment before trying again.'
        })
        break
        
      case 500:
      case 502:
      case 503:
      case 504:
        // Server errors
        showNotification({
          type: 'error',
          title: 'Server Error',
          message: 'Server error. Please try again later.'
        })
        break
        
      default:
        // Generic error
        showNotification({
          type: 'error',
          title: 'Error',
          message: data?.detail || 'An unexpected error occurred. Please try again.'
        })
    }
    
    return Promise.reject(error)
  }
)

// API methods
export const api = {
  // Authentication
  auth: {
    login: (credentials: { email: string; password: string; two_factor_code?: string }) =>
      apiService.post('/login/', credentials),
    
    register: (data: { email: string; password: string; full_name: string; phone_number?: string; email_notifications?: boolean }) =>
      apiService.post('/register/', data),
    
    logout: () =>
      apiService.post('/logout/'),
    
    refreshToken: (refresh: string) =>
      apiService.post('/token/refresh/', { refresh }),
    
    getToken: (credentials: { email: string; password: string }) =>
      apiService.post('/token/', credentials),
    
    getProfile: () =>
      apiService.get('/profile/'),
    
    updateProfile: (data: any) =>
      apiService.put('/profile/', data),
    
    changePassword: (data: { current_password: string; new_password: string }) =>
      apiService.post('/password/change/', data),
    
    getLoginHistory: () =>
      apiService.get('/login-history/'),
    
    getSettings: () =>
      apiService.get('/settings/'),
    
    updateSettings: (data: any) =>
      apiService.put('/settings/', data)
  },
  
  // Trading Engine
  trading: {
    getPriceFeed: (symbol?: string) =>
      apiService.get('/trading/price_feed/', { params: symbol ? { symbol } : {} }),
    
    getMarketData: (symbol?: string) =>
      apiService.get('/trading/market_data/', { params: symbol ? { symbol } : {} }),
    
    getOrderBook: (symbol?: string, depth?: number) =>
      apiService.get('/trading/order_book/', { params: { symbol, depth } }),
    
    getTradingSignals: (symbol?: string) =>
      apiService.get('/trading/trading_signal/', { params: symbol ? { symbol } : {} }),
    
    executeTrade: (data: {
      symbol: string;
      side: 'buy' | 'sell';
      order_type: 'market' | 'limit' | 'stop' | 'stop_limit';
      quantity: number;
      price?: number;
      stop_price?: number;
      time_in_force?: 'day' | 'gtc' | 'ioc' | 'fok';
    }) =>
      apiService.post('/trading/execute_trade/', data),
    
    getStrategies: () =>
      apiService.get('/trading/strategies/')
  },
  
  // Trades
  trades: {
    getTrades: (params: any = {}) =>
      apiService.get('/trades/', { params }),
    
    createTrade: (data: any) =>
      apiService.post('/trades/', data),
    
    getTrade: (id: number) =>
      apiService.get(`/trades/${id}/`),
    
    cancelTrade: (id: number) =>
      apiService.post(`/trades/${id}/cancel/`),
    
    getTradeStats: () =>
      apiService.get('/trades/stats/'),
    
    getTradeHistory: (params: any = {}) =>
      apiService.get('/trades/history/', { params }),
    
    // Crypto specific endpoints
    getCryptocurrencies: () =>
      apiService.get('/cryptocurrencies/'),
    
    getCryptocurrency: (id: number) =>
      apiService.get(`/cryptocurrencies/${id}/`),
    
    executeCryptoTrade: (data: any) =>
      apiService.post('/execute-trade/', data),
    
    getCryptoPriceFeed: (symbol?: string) =>
      apiService.get('/price-feed/', { params: symbol ? { symbol } : {} }),
    
    getTradingSignals: (symbol?: string) =>
      apiService.get('/trading-signals/', { params: symbol ? { symbol } : {} }),
    
    getTradingStats: () =>
      apiService.get('/trading-stats/')
  },
  
  // Wallets & Portfolio
  wallets: {
    getWallet: () =>
      apiService.get('/wallet/'),
    
    getBalance: () =>
      apiService.get('/wallet/'),
    
    getTransactions: (params: any = {}) =>
      apiService.get('/transactions/', { params }),
    
    withdraw: (data: { amount: string; to_address: string }) =>
      apiService.post('/withdraw/', data),
    
    checkDeposit: () =>
      apiService.post('/deposit_check/'),
    
    // Crypto wallet endpoints
    getCryptoWallets: () =>
      apiService.get('/crypto-wallets/'),
    
    getCryptoWallet: (id: number) =>
      apiService.get(`/crypto-wallets/${id}/`),
    
    getWalletBalances: () =>
      apiService.get('/wallet-balances/'),
    
    // Crypto swaps
    getCryptoSwaps: () =>
      apiService.get('/crypto-swaps/'),
    
    getSwapQuote: (data: { from_token: string; to_token: string; amount: string }) =>
      apiService.post('/swap-quote/', data),
    
    executeSwap: (data: any) =>
      apiService.post('/execute-swap/', data),
    
    getSupportedTokens: () =>
      apiService.get('/supported-tokens/'),
    
    getSwapPairs: () =>
      apiService.get('/swap-pairs/'),
    
    // Deposits and withdrawals
    getDeposits: () =>
      apiService.get('/deposits/'),
    
    getWithdrawals: () =>
      apiService.get('/withdrawals/'),
    
    requestWithdrawal: (data: any) =>
      apiService.post('/request-withdrawal/', data)
  },
  
  // Notifications
  notifications: {
    getNotifications: () =>
      apiService.get('/notifications/'),
    
    getNotification: (id: number) =>
      apiService.get(`/notifications/${id}/`),
    
    markAsRead: (id: number) =>
      apiService.patch(`/notifications/${id}/`, { is_read: true })
  },
  
  // Crypto Investments
  investments: {
    // Crypto Indices
    getCryptoIndices: () =>
      apiService.get('/trades/crypto-indices/'),
    
    getCryptoIndex: (id: number) =>
      apiService.get(`/trades/crypto-indices/${id}/`),
    
    getIndexPriceHistory: (indexId: number, days: number = 30) =>
      apiService.get(`/trades/crypto-indices/${indexId}/price-history/`, { params: { days } }),
    
    // Investments
    getInvestments: () =>
      apiService.get('/trades/investments/'),
    
    createInvestment: (data: any) =>
      apiService.post('/trades/investments/', data),
    
    getInvestment: (id: number) =>
      apiService.get(`/trades/investments/${id}/`),
    
    updateInvestment: (id: number, data: any) =>
      apiService.put(`/trades/investments/${id}/`, data),
    
    closeInvestment: (id: number) =>
      apiService.delete(`/trades/investments/${id}/`),
    
    // Investment transactions
    addFunds: (investmentId: number, data: { amount_btc: number; notes?: string }) =>
      apiService.post(`/trades/investments/${investmentId}/add-funds/`, {
        transaction_type: 'deposit',
        ...data
      }),
    
    withdrawFunds: (investmentId: number, data: { amount_btc: number; notes?: string }) =>
      apiService.post(`/trades/investments/${investmentId}/withdraw/`, {
        transaction_type: 'withdraw',
        ...data
      }),
    
    getInvestmentPerformance: (investmentId: number) =>
      apiService.get(`/trades/investments/${investmentId}/performance/`),
    
    getInvestmentHistory: (investmentId: number) =>
      apiService.get(`/trades/investments/${investmentId}/history/`),
    
    // Portfolio analytics
    getPortfolioAllocation: () =>
      apiService.get('/trades/portfolio/allocation/')
  },
  
  // Admin Control APIs
  admin: {
    // Trading Settings
    getTradingSettings: () =>
      apiService.get('/admin/settings/'),
    
    updateTradingSettings: (data: any) =>
      apiService.put('/admin/settings/', data),
    
    // Dashboard Statistics
    getDashboardStats: () =>
      apiService.get('/admin/dashboard-stats/'),
    
    getSystemHealth: () =>
      apiService.get('/admin/system-health/'),
    
    // Price Control
    executeManualPriceControl: (data: {
      cryptocurrency_id?: number;
      crypto_index_id?: number;
      price_change_percent: number;
      duration_seconds?: number;
    }) =>
      apiService.post('/admin/manual-price-control/', data),
    
    // Profit/Loss Scenarios
    getScenarios: () =>
      apiService.get('/admin/scenarios/'),
    
    createScenario: (data: any) =>
      apiService.post('/admin/scenarios/', data),
    
    getScenario: (id: number) =>
      apiService.get(`/admin/scenarios/${id}/`),
    
    updateScenario: (id: number, data: any) =>
      apiService.put(`/admin/scenarios/${id}/`, data),
    
    deleteScenario: (id: number) =>
      apiService.delete(`/admin/scenarios/${id}/`),
    
    executeScenario: (id: number) =>
      apiService.post(`/admin/execute-scenario/${id}/`),
    
    // Deposit Management
    getDepositWallets: () =>
      apiService.get('/admin/deposit-wallets/'),
    
    createDepositWallet: (data: any) =>
      apiService.post('/admin/deposit-wallets/', data),
    
    getPendingDeposits: () =>
      apiService.get('/admin/pending-deposits/'),
    
    approveDeposit: (id: number, notes?: string) =>
      apiService.post(`/admin/approve-deposit/${id}/`, { notes: notes || 'Approved by admin' }),
    
    rejectDeposit: (id: number, notes?: string) =>
      apiService.post(`/admin/reject-deposit/${id}/`, { notes: notes || 'Rejected by admin' }),
    
    // Price Movement Logs
    getPriceMovements: (params?: { hours?: number; movement_type?: string }) =>
      apiService.get('/admin/price-movements/', { params }),
    
    // System Monitoring
    getAutomatedTasks: (params?: any) =>
      apiService.get('/admin/automated-tasks/', { params })
  }
}

export { apiService }
export default apiService