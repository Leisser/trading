import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export interface PriceData {
  binance: number
  coingecko: number
  timestamp: string
}

export interface TradeSignal {
  signal: 'buy' | 'sell' | 'hold'
  timestamp: string
}

export interface Trade {
  id: number
  trade_type: 'buy' | 'sell'
  btc_amount: string
  usd_price: string
  timestamp: string
  status: string
}

export interface Wallet {
  address: string
  balance: string
  label: string
}

export const useTradingStore = defineStore('trading', () => {
  const currentPrice = ref<PriceData | null>(null)
  const tradeSignal = ref<TradeSignal | null>(null)
  const trades = ref<Trade[]>([])
  const wallet = ref<Wallet | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // WebSocket connection for real-time price feed
  let priceWebSocket: WebSocket | null = null

  // Connect to price feed WebSocket
  const connectPriceFeed = () => {
    try {
      priceWebSocket = new WebSocket('ws://localhost:8000/ws/price_feed/')
      
      priceWebSocket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        currentPrice.value = {
          ...data,
          timestamp: new Date().toISOString()
        }
      }

      priceWebSocket.onerror = (error) => {
        console.error('WebSocket error:', error)
        error.value = 'Failed to connect to price feed'
      }

      priceWebSocket.onclose = () => {
        console.log('Price feed WebSocket closed')
      }
    } catch (err) {
      console.error('Failed to connect to WebSocket:', err)
    }
  }

  // Disconnect WebSocket
  const disconnectPriceFeed = () => {
    if (priceWebSocket) {
      priceWebSocket.close()
      priceWebSocket = null
    }
  }

  // Get current price from REST API
  const fetchCurrentPrice = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/trading/price_feed/')
      currentPrice.value = {
        binance: response.data.close,
        coingecko: response.data.close,
        timestamp: new Date().toISOString()
      }
    } catch (err) {
      console.error('Failed to fetch price:', err)
    }
  }

  // Get trading signal
  const fetchTradeSignal = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/trading/trading_signal/')
      tradeSignal.value = {
        signal: response.data.signal,
        timestamp: new Date().toISOString()
      }
    } catch (err) {
      console.error('Failed to fetch trade signal:', err)
    }
  }

  // Execute trade
  const executeTrade = async (tradeData: {
    amount: number
    leverage: number
    trade_type: 'buy' | 'sell'
  }) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('http://localhost:8000/api/trading/execute_trade/', tradeData)
      
      if (response.data.status === 'Trade executed (simulated)') {
        // Refresh trades list
        await fetchTrades()
        return { success: true, data: response.data }
      } else {
        error.value = response.data.error || 'Trade execution failed'
        return { success: false, error: error.value }
      }
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Trade execution failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Fetch user's trades
  const fetchTrades = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/trades/')
      trades.value = response.data.results || response.data
    } catch (err) {
      console.error('Failed to fetch trades:', err)
    }
  }

  // Fetch user's wallet
  const fetchWallet = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/wallet/')
      wallet.value = response.data
    } catch (err) {
      console.error('Failed to fetch wallet:', err)
    }
  }

  // Create a simple trade (legacy endpoint)
  const createTrade = async (tradeData: {
    trade_type: 'buy' | 'sell'
    btc_amount: string
    usd_price: string
  }) => {
    try {
      const response = await axios.post('http://localhost:8000/api/trades/', tradeData)
      await fetchTrades()
      return { success: true, data: response.data }
    } catch (err: any) {
      return { 
        success: false, 
        error: err.response?.data || 'Failed to create trade' 
      }
    }
  }

  // Request withdrawal
  const requestWithdrawal = async (withdrawalData: {
    amount: string
    to_address: string
  }) => {
    try {
      const response = await axios.post('http://localhost:8000/api/withdraw/', withdrawalData)
      return { success: true, data: response.data }
    } catch (err: any) {
      return { 
        success: false, 
        error: err.response?.data || 'Withdrawal request failed' 
      }
    }
  }

  // Check deposits
  const checkDeposits = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/deposit_check/')
      await fetchWallet()
      return { success: true, data: response.data }
    } catch (err: any) {
      return { 
        success: false, 
        error: err.response?.data || 'Failed to check deposits' 
      }
    }
  }

  return {
    currentPrice,
    tradeSignal,
    trades,
    wallet,
    loading,
    error,
    connectPriceFeed,
    disconnectPriceFeed,
    fetchCurrentPrice,
    fetchTradeSignal,
    executeTrade,
    fetchTrades,
    fetchWallet,
    createTrade,
    requestWithdrawal,
    checkDeposits
  }
}) 