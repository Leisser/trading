import { ref, computed } from 'vue'

// Types
export interface CandlestickData {
  timestamp: number
  open: number
  high: number
  low: number
  close: number
  volume: number
}

export interface SpotBuy {
  id: number
  crypto: string
  amount: number
  entryPrice: number
  currentPrice: number
  currentValue: number
  pnl: number
  entryDate: Date
  performance: number
}

export interface LiveUpdate {
  crypto: string
  price: number
  change: number
  changePercent: number
  timestamp: Date
}

// Mock data store
const liveData = ref<Map<string, CandlestickData[]>>(new Map())
const spotBuys = ref<SpotBuy[]>([])
const isConnected = ref(false)
const updateInterval = ref<NodeJS.Timeout | null>(null)

// Crypto price simulation
const cryptoPrices = ref<Map<string, number>>(
  new Map([
    ['BTC', 46500],
    ['ETH', 3150],
    ['SOL', 102],
    ['ADA', 0.45],
    ['DOT', 6.8],
    ['LINK', 15.2],
  ]),
)

// Price volatility for realistic simulation
const volatilityRanges = {
  BTC: { min: 0.005, max: 0.02 },
  ETH: { min: 0.008, max: 0.025 },
  SOL: { min: 0.01, max: 0.03 },
  ADA: { min: 0.015, max: 0.035 },
  DOT: { min: 0.012, max: 0.028 },
  LINK: { min: 0.01, max: 0.025 },
}

// Generate realistic price movement
const generatePriceMovement = (crypto: string, currentPrice: number): number => {
  const volatility = volatilityRanges[crypto as keyof typeof volatilityRanges]
  const changePercent =
    (Math.random() - 0.5) * 2 * (volatility.min + Math.random() * (volatility.max - volatility.min))
  return currentPrice * (1 + changePercent)
}

// Generate candlestick data
const generateCandlestick = (crypto: string, basePrice: number): CandlestickData => {
  const now = Date.now()
  const volatility = volatilityRanges[crypto as keyof typeof volatilityRanges]
  const maxChange = basePrice * (volatility.min + Math.random() * (volatility.max - volatility.min))

  const open = basePrice
  const close = basePrice + (Math.random() - 0.5) * maxChange
  const high = Math.max(open, close) + Math.random() * maxChange * 0.5
  const low = Math.min(open, close) - Math.random() * maxChange * 0.5
  const volume = Math.random() * 1000000 + 500000

  return {
    timestamp: now,
    open,
    high,
    low,
    close,
    volume,
  }
}

// Initialize historical data for a crypto
const initializeHistoricalData = (crypto: string): void => {
  const basePrice = cryptoPrices.value.get(crypto) || 100
  const data: CandlestickData[] = []

  // Generate 100 historical candles (5-minute intervals)
  for (let i = 100; i >= 0; i--) {
    const timestamp = Date.now() - i * 5 * 60 * 1000
    const candle = generateCandlestick(crypto, basePrice)
    candle.timestamp = timestamp
    data.push(candle)

    // Update base price for next candle
    cryptoPrices.value.set(crypto, candle.close)
  }

  liveData.value.set(crypto, data)
}

// Update live data
const updateLiveData = (): void => {
  cryptoPrices.value.forEach((price, crypto) => {
    const newPrice = generatePriceMovement(crypto, price)
    cryptoPrices.value.set(crypto, newPrice)

    const candle = generateCandlestick(crypto, newPrice)
    const data = liveData.value.get(crypto) || []

    // Add new candle
    data.push(candle)

    // Keep only last 100 candles
    if (data.length > 100) {
      data.shift()
    }

    liveData.value.set(crypto, data)
  })

  // Update spot buys
  updateSpotBuys()
}

// Update spot buy values
const updateSpotBuys = (): void => {
  spotBuys.value.forEach((spotBuy) => {
    const currentPrice = cryptoPrices.value.get(spotBuy.crypto) || spotBuy.currentPrice
    spotBuy.currentPrice = currentPrice
    spotBuy.currentValue = spotBuy.amount * currentPrice
    spotBuy.pnl = spotBuy.currentValue - spotBuy.amount * spotBuy.entryPrice
    spotBuy.performance = ((currentPrice - spotBuy.entryPrice) / spotBuy.entryPrice) * 100
  })
}

// Public API
export const useLiveDataService = () => {
  // Connect to live data
  const connect = (): void => {
    if (isConnected.value) return

    // Initialize data for all cryptos
    cryptoPrices.value.forEach((_, crypto) => {
      initializeHistoricalData(crypto)
    })

    // Start live updates every 2 seconds
    updateInterval.value = setInterval(() => {
      updateLiveData()
    }, 2000)

    isConnected.value = true
  }

  // Disconnect from live data
  const disconnect = (): void => {
    if (updateInterval.value) {
      clearInterval(updateInterval.value)
      updateInterval.value = null
    }
    isConnected.value = false
  }

  // Get candlestick data for a crypto
  const getCandlestickData = (crypto: string): CandlestickData[] => {
    return liveData.value.get(crypto) || []
  }

  // Get current price for a crypto
  const getCurrentPrice = (crypto: string): number => {
    return cryptoPrices.value.get(crypto) || 0
  }

  // Get all current prices
  const getAllPrices = computed(() => {
    const prices: LiveUpdate[] = []
    cryptoPrices.value.forEach((price, crypto) => {
      const data = liveData.value.get(crypto) || []
      const previousPrice = data.length > 1 ? data[data.length - 2].close : price
      const change = price - previousPrice
      const changePercent = ((price - previousPrice) / previousPrice) * 100

      prices.push({
        crypto,
        price,
        change,
        changePercent,
        timestamp: new Date(),
      })
    })
    return prices
  })

  // Add spot buy
  const addSpotBuy = (spotBuy: Omit<SpotBuy, 'id'>): number => {
    const id = Date.now()
    const newSpotBuy: SpotBuy = {
      ...spotBuy,
      id,
      currentPrice: cryptoPrices.value.get(spotBuy.crypto) || spotBuy.entryPrice,
      currentValue: spotBuy.amount * (cryptoPrices.value.get(spotBuy.crypto) || spotBuy.entryPrice),
      pnl: 0,
      performance: 0,
    }

    spotBuys.value.push(newSpotBuy)
    updateSpotBuys()
    return id
  }

  // Update spot buy
  const updateSpotBuy = (id: number, updates: Partial<SpotBuy>): void => {
    const index = spotBuys.value.findIndex((sb) => sb.id === id)
    if (index !== -1) {
      spotBuys.value[index] = { ...spotBuys.value[index], ...updates }
      updateSpotBuys()
    }
  }

  // Remove spot buy
  const removeSpotBuy = (id: number): void => {
    const index = spotBuys.value.findIndex((sb) => sb.id === id)
    if (index !== -1) {
      spotBuys.value.splice(index, 1)
    }
  }

  // Get all spot buys
  const getSpotBuys = computed(() => spotBuys.value)

  // Get connection status
  const getConnectionStatus = computed(() => isConnected.value)

  // Subscribe to price updates
  const subscribeToUpdates = (callback: (updates: LiveUpdate[]) => void): (() => void) => {
    const interval = setInterval(() => {
      if (isConnected.value) {
        callback(getAllPrices.value)
      }
    }, 2000)

    return () => clearInterval(interval)
  }

  return {
    connect,
    disconnect,
    getCandlestickData,
    getCurrentPrice,
    getAllPrices,
    addSpotBuy,
    updateSpotBuy,
    removeSpotBuy,
    getSpotBuys,
    getConnectionStatus,
    subscribeToUpdates,
  }
}

// Initialize with some sample spot buys
spotBuys.value = [
  {
    id: 1,
    crypto: 'BTC',
    amount: 0.5,
    entryPrice: 45000,
    currentPrice: 46500,
    currentValue: 23250,
    pnl: 750,
    entryDate: new Date('2024-01-15T10:30:00Z'),
    performance: 1.67,
  },
  {
    id: 2,
    crypto: 'ETH',
    amount: 5.0,
    entryPrice: 3200,
    currentPrice: 3150,
    currentValue: 15750,
    pnl: -250,
    entryDate: new Date('2024-01-16T14:20:00Z'),
    performance: -1.56,
  },
  {
    id: 3,
    crypto: 'SOL',
    amount: 50.0,
    entryPrice: 95,
    currentPrice: 102,
    currentValue: 5100,
    pnl: 350,
    entryDate: new Date('2024-01-17T09:15:00Z'),
    performance: 7.37,
  },
]
