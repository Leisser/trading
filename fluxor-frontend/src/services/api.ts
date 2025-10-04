import axios from 'axios'
import { PersistenceService } from './persistenceService'

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    const persistenceService = PersistenceService.getInstance()
    const authData = await persistenceService.loadAuthData()

    if (authData?.access) {
      config.headers.Authorization = `Bearer ${authData.access}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor to handle common errors and token refresh
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // Handle 401 errors with token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const tokens = localStorage.getItem('auth_tokens')
      if (tokens) {
        try {
          const persistenceService = PersistenceService.getInstance()
          const authData = await persistenceService.loadAuthData()

          if (authData?.refresh) {
            const response = await api.post('/refresh/', { refresh: authData.refresh })
            const { access, refresh } = response.data

            // Update stored tokens
            await persistenceService.saveAuthData({
              access,
              refresh: refresh || authData.refresh,
              user: authData.user,
            })

            // Retry original request with new token
            originalRequest.headers.Authorization = `Bearer ${access}`
            return api(originalRequest)
          }
        } catch (refreshError) {
          // Refresh failed, clear tokens and redirect to login
          const persistenceService = PersistenceService.getInstance()
          await persistenceService.clearAuthData()
          if (window.location.pathname !== '/login') {
            window.location.href = '/login'
          }
        }
      } else {
        // No tokens, redirect to login
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      }
    }

    // Handle 403 errors (forbidden) - could be invalid token
    if (error.response?.status === 403) {
      console.warn('Access forbidden, clearing auth data')
      const persistenceService = PersistenceService.getInstance()
      await persistenceService.clearAuthData()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  },
)

// Auth API methods
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/login/', { email, password })
    return response.data
  },

  register: async (userData: {
    email: string
    full_name: string
    password: string
    password_confirm: string
    phone_number?: string
  }) => {
    const response = await api.post('/register/', userData)
    return response.data
  },

  getUser: async () => {
    const response = await api.get('/user/')
    return response.data
  },

  refreshToken: async (refreshToken: string) => {
    const response = await api.post('/refresh/', { refresh: refreshToken })
    return response.data
  },

  changePassword: async (data: { current_password: string; new_password: string }) => {
    const response = await api.post('/change_password/', data)
    return response.data
  },

  socialAuth: async (data: {
    provider: 'google' | 'apple'
    access_token: string
    user_data?: Record<string, unknown>
  }) => {
    const response = await api.post('/social-auth/', data)
    return response.data
  },

  firebaseAuth: async (data: {
    id_token: string
    firebase_user?: {
      uid: string
      email: string | null
      displayName: string | null
      photoURL: string | null
      emailVerified: boolean
      phoneNumber: string | null
    }
  }) => {
    const response = await api.post('/firebase-auth/', data)
    return response.data
  },

  firebaseDashboardAuth: async (data: {
    id_token: string
    firebase_user?: {
      uid: string
      email: string | null
      displayName: string | null
      photoURL: string | null
      emailVerified: boolean
      phoneNumber: string | null
    }
  }) => {
    const response = await api.post('/firebase-dashboard-auth/', data)
    return response.data
  },

  refreshFirebaseSession: async (data: {
    refresh: string
    user_id: string
  }) => {
    const response = await api.post('/firebase-refresh/', data)
    return response.data
  },

  sendPhoneVerification: async (phoneNumber: string) => {
    const response = await api.post('/phone-verification/', {
      phone_number: phoneNumber,
    })
    return response.data
  },

  verifyPhoneCode: async (phoneNumber: string, code: string) => {
    const response = await api.put('/phone-verification/', {
      phone_number: phoneNumber,
      verification_code: code,
    })
    return response.data
  },

  logout: async () => {
    const response = await api.post('/logout/')
    return response.data
  },
}

// Trading API methods - Updated to use consolidated fluxor_api endpoints
export const tradingAPI = {
  getPriceFeed: async () => {
    const response = await api.get('/trades/price-feed/')
    return response.data
  },

  getTradingSignal: async () => {
    const response = await api.get('/trades/trading-signals/')
    return response.data
  },

  executeTrade: async (tradeData: {
    cryptocurrency_id: number
    amount: number
    leverage: number
    trade_type: 'buy' | 'sell'
  }) => {
    const response = await api.post('/trades/execute-trade/', tradeData)
    return response.data
  },

  getTrades: async () => {
    const response = await api.get('/trades/trades/')
    return response.data
  },

  createTrade: async (tradeData: {
    trade_type: 'buy' | 'sell'
    btc_amount: string
    usd_price: string
  }) => {
    const response = await api.post('/trades/trades/', tradeData)
    return response.data
  },

  getWallet: async () => {
    const response = await api.get('/trades/wallet/')
    return response.data
  },

  requestWithdrawal: async (withdrawalData: { amount: string; to_address: string }) => {
    const response = await api.post('/trades/request-withdrawal/', withdrawalData)
    return response.data
  },

  checkDeposits: async () => {
    const response = await api.post('/trades/check-deposits/')
    return response.data
  },

  // New enhanced crypto endpoints
  getCryptocurrencies: async () => {
    const response = await api.get('/trades/cryptocurrencies/')
    return response.data
  },

  getCryptoWallets: async () => {
    const response = await api.get('/trades/crypto-wallets/')
    return response.data
  },

  createCryptoWallet: async (walletType: string) => {
    const response = await api.post('/trades/crypto-wallets/', { wallet_type: walletType })
    return response.data
  },

  getWalletBalances: async () => {
    const response = await api.get('/trades/wallet-balances/')
    return response.data
  },

  getCryptoSwaps: async () => {
    const response = await api.get('/trades/crypto-swaps/')
    return response.data
  },

  getSwapQuote: async (fromTokenId: number, toTokenId: number, amount: number) => {
    const response = await api.post('/trades/swap-quote/', {
      from_cryptocurrency_id: fromTokenId,
      to_cryptocurrency_id: toTokenId,
      from_amount: amount
    })
    return response.data
  },

  executeSwap: async (fromTokenId: number, toTokenId: number, amount: number) => {
    const response = await api.post('/trades/execute-swap/', {
      from_cryptocurrency_id: fromTokenId,
      to_cryptocurrency_id: toTokenId,
      from_amount: amount
    })
    return response.data
  },

  getSupportedTokens: async () => {
    const response = await api.get('/trades/supported-tokens/')
    return response.data
  },

  getSwapPairs: async () => {
    const response = await api.get('/trades/swap-pairs/')
    return response.data
  },

  getCryptoPayments: async () => {
    const response = await api.get('/trades/crypto-payments/')
    return response.data
  },

  createPayment: async (amountUsd: number, cryptocurrency: string) => {
    const response = await api.post('/trades/create-payment/', {
      amount_usd: amountUsd,
      cryptocurrency: cryptocurrency
    })
    return response.data
  },

  verifyPayment: async (paymentId: string, transactionHash: string) => {
    const response = await api.post('/trades/verify-payment/', {
      payment_id: paymentId,
      transaction_hash: transactionHash
    })
    return response.data
  },

  getTradingStats: async () => {
    const response = await api.get('/trades/trading-stats/')
    return response.data
  },

  getNotifications: async () => {
    const response = await api.get('/trades/notifications/')
    return response.data
  },

  getDeposits: async () => {
    const response = await api.get('/trades/deposits/')
    return response.data
  },

  getWithdrawals: async () => {
    const response = await api.get('/trades/withdrawals/')
    return response.data
  },
}

// Profile API methods
export const profileAPI = {
  updateProfile: async (profileData: any) => {
    const response = await api.patch('/user/', profileData)
    return response.data
  },

  updateSettings: async (settings: any) => {
    const response = await api.patch('/user/settings/', settings)
    return response.data
  },

  uploadKYC: async (formData: FormData) => {
    const response = await api.post('/kyc_upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  getLoginHistory: async () => {
    const response = await api.get('/login_history/')
    return response.data
  },
}

// Admin API methods
export const adminAPI = {
  getUsers: async () => {
    const response = await api.get('/accounts/users/')
    return response.data
  },
}

export default api
