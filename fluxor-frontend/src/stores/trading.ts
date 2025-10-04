import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

interface CryptoWallet {
  id: number
  wallet_type: string
  address: string
  balance: number
  label: string
  is_active: boolean
  created_at: string
}

interface CryptoSwap {
  id: number
  from_cryptocurrency_symbol: string
  to_cryptocurrency_symbol: string
  from_amount: number
  to_amount: number
  exchange_rate: number
  network_fee: number
  status: string
  transaction_hash: string
  swap_provider: string
  executed_at: string
  created_at: string
}

interface CryptoPayment {
  id: number
  payment_id: string
  amount_usd: number
  amount_crypto: number
  cryptocurrency_symbol: string
  payment_provider: string
  payment_url: string
  wallet_address: string
  status: string
  expires_at: string
  created_at: string
}

interface SwapQuote {
  from_token: string
  to_token: string
  from_amount: number
  to_amount: number
  exchange_rate: number
  network_fee: number
  provider: string
  estimated_time: string
}

interface WalletBalance {
  wallet_type: string
  address: string
  balance: number
  usd_value: number
  price_usd: number
}

interface SupportedToken {
  id: number
  symbol: string
  name: string
  current_price: number
}

interface SwapPair {
  from: string
  to: string
}

export const useTradingStore = defineStore('trading', () => {
  const authStore = useAuthStore()

  // State
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPrice = ref<any>(null)
  const priceFeed = ref<any[]>([])
  const trades = ref<any[]>([])
  const cryptoWallets = ref<CryptoWallet[]>([])
  const cryptoSwaps = ref<CryptoSwap[]>([])
  const cryptoPayments = ref<CryptoPayment[]>([])
  const walletBalances = ref<WalletBalance[]>([])
  const supportedTokens = ref<SupportedToken[]>([])
  const swapPairs = ref<SwapPair[]>([])
  const priceWebSocket = ref<WebSocket | null>(null)

  // Computed
  const totalPortfolioValue = computed(() => {
    return walletBalances.value.reduce((total, wallet) => total + wallet.usd_value, 0)
  })

  const totalTrades = computed(() => trades.value.length)

  const winRate = computed(() => {
    if (trades.value.length === 0) return 0
    const winningTrades = trades.value.filter((trade) => trade.pnl > 0)
    return (winningTrades.length / trades.value.length) * 100
  })

  const totalPnL = computed(() => {
    return trades.value.reduce((total, trade) => total + (trade.pnl || 0), 0)
  })

  // Actions
  const fetchPriceFeed = async () => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/price-feed/`, {
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        priceFeed.value = await response.json()
      } else {
        throw new Error('Failed to fetch price feed')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch price feed'
    } finally {
      loading.value = false
    }
  }

  const fetchTrades = async () => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/trades/`, {
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        trades.value = await response.json()
      } else {
        throw new Error('Failed to fetch trades')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch trades'
    } finally {
      loading.value = false
    }
  }

  const executeTrade = async (tradeData: any) => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/execute-trade/`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tradeData),
      })

      if (response.ok) {
        const result = await response.json()
        await fetchTrades() // Refresh trades
        return result
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to execute trade')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to execute trade'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Crypto Wallet Management
  const fetchCryptoWallets = async () => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/crypto-wallets/`, {
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        cryptoWallets.value = await response.json()
      } else {
        throw new Error('Failed to fetch crypto wallets')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch crypto wallets'
    } finally {
      loading.value = false
    }
  }

  const createCryptoWallet = async (walletType: string) => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/crypto-wallets/`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ wallet_type: walletType }),
      })

      if (response.ok) {
        const newWallet = await response.json()
        cryptoWallets.value.push(newWallet)
        return newWallet
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to create wallet')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create wallet'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchWalletBalances = async () => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/wallet-balances/`, {
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        walletBalances.value = await response.json()
      } else {
        throw new Error('Failed to fetch wallet balances')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch wallet balances'
    } finally {
      loading.value = false
    }
  }

  // Crypto Swaps
  const fetchCryptoSwaps = async () => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/crypto-swaps/`, {
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        cryptoSwaps.value = await response.json()
      } else {
        throw new Error('Failed to fetch crypto swaps')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch crypto swaps'
    } finally {
      loading.value = false
    }
  }

  const getSwapQuote = async (
    fromTokenId: number,
    toTokenId: number,
    amount: number,
  ): Promise<SwapQuote> => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/swap-quote/`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from_cryptocurrency_id: fromTokenId,
          to_cryptocurrency_id: toTokenId,
          from_amount: amount,
        }),
      })

      if (response.ok) {
        return await response.json()
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to get swap quote')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to get swap quote'
      throw err
    } finally {
      loading.value = false
    }
  }

  const executeSwap = async (fromTokenId: number, toTokenId: number, amount: number) => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/execute-swap/`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from_cryptocurrency_id: fromTokenId,
          to_cryptocurrency_id: toTokenId,
          from_amount: amount,
        }),
      })

      if (response.ok) {
        const result = await response.json()
        await fetchCryptoSwaps() // Refresh swaps
        await fetchWalletBalances() // Refresh balances
        return result
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to execute swap')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to execute swap'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchSupportedTokens = async () => {
    try {
      loading.value = true
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/trades/supported-tokens/`,
        {
          headers: {
            Authorization: `Token ${authStore.token}`,
            'Content-Type': 'application/json',
          },
        },
      )

      if (response.ok) {
        supportedTokens.value = await response.json()
      } else {
        throw new Error('Failed to fetch supported tokens')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch supported tokens'
    } finally {
      loading.value = false
    }
  }

  const fetchSwapPairs = async () => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/swap-pairs/`, {
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        swapPairs.value = await response.json()
      } else {
        throw new Error('Failed to fetch swap pairs')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch swap pairs'
    } finally {
      loading.value = false
    }
  }

  // Crypto Payments
  const fetchCryptoPayments = async () => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/crypto-payments/`, {
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        cryptoPayments.value = await response.json()
      } else {
        throw new Error('Failed to fetch crypto payments')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch crypto payments'
    } finally {
      loading.value = false
    }
  }

  const createPayment = async (amountUsd: number, cryptocurrency: string) => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/create-payment/`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount_usd: amountUsd,
          cryptocurrency: cryptocurrency,
        }),
      })

      if (response.ok) {
        const result = await response.json()
        await fetchCryptoPayments() // Refresh payments
        return result
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to create payment')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create payment'
      throw err
    } finally {
      loading.value = false
    }
  }

  const verifyPayment = async (paymentId: string, transactionHash: string) => {
    try {
      loading.value = true
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/trades/verify-payment/`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${authStore.tokens?.access}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          payment_id: paymentId,
          transaction_hash: transactionHash,
        }),
      })

      if (response.ok) {
        const result = await response.json()
        await fetchCryptoPayments() // Refresh payments
        return result
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to verify payment')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to verify payment'
      throw err
    } finally {
      loading.value = false
    }
  }

  // WebSocket for real-time price updates
  const connectPriceFeed = () => {
    if (priceWebSocket.value) {
      priceWebSocket.value.close()
    }

    const wsUrl = `${import.meta.env.VITE_WS_URL}/ws/price/`
    priceWebSocket.value = new WebSocket(wsUrl)

    priceWebSocket.value.onopen = () => {
      console.log('Connected to price feed WebSocket')
    }

    priceWebSocket.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'price_update') {
          // Update price feed with new data
          const index = priceFeed.value.findIndex((item) => item.symbol === data.symbol)
          if (index !== -1) {
            priceFeed.value[index] = { ...priceFeed.value[index], ...data }
          }
        }
      } catch (err) {
        console.error('Error parsing WebSocket message:', err)
      }
    }

    priceWebSocket.value.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    priceWebSocket.value.onclose = () => {
      console.log('Disconnected from price feed WebSocket')
    }
  }

  const disconnectPriceFeed = () => {
    if (priceWebSocket.value) {
      priceWebSocket.value.close()
      priceWebSocket.value = null
    }
  }

  // Initialize data
  const initializeData = async () => {
    await Promise.all([
      fetchPriceFeed(),
      fetchTrades(),
      fetchCryptoWallets(),
      fetchCryptoSwaps(),
      fetchCryptoPayments(),
      fetchWalletBalances(),
      fetchSupportedTokens(),
      fetchSwapPairs(),
    ])
  }

  return {
    // State
    loading,
    error,
    currentPrice,
    priceFeed,
    trades,
    cryptoWallets,
    cryptoSwaps,
    cryptoPayments,
    walletBalances,
    supportedTokens,
    swapPairs,

    // Computed
    totalPortfolioValue,
    totalTrades,
    winRate,
    totalPnL,

    // Actions
    fetchPriceFeed,
    fetchTrades,
    executeTrade,
    fetchCryptoWallets,
    createCryptoWallet,
    fetchWalletBalances,
    fetchCryptoSwaps,
    getSwapQuote,
    executeSwap,
    fetchSupportedTokens,
    fetchSwapPairs,
    fetchCryptoPayments,
    createPayment,
    verifyPayment,
    connectPriceFeed,
    disconnectPriceFeed,
    initializeData,
  }
})
