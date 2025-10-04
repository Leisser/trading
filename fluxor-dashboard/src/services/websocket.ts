import { ref, reactive } from 'vue'

interface WebSocketMessage {
  type: string
  data: any
  timestamp: number
}

interface PriceUpdate {
  symbol: string
  price: number
  change: number
  volume: number
  timestamp: number
}

interface TradeUpdate {
  id: string
  userId: number
  symbol: string
  type: 'buy' | 'sell'
  amount: number
  price: number
  status: 'pending' | 'filled' | 'cancelled'
  timestamp: number
}

interface PaymentUpdate {
  id: number
  userId: number
  type: 'deposit' | 'withdrawal'
  amount: number
  status: 'pending' | 'approved' | 'rejected'
  timestamp: number
}

class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectInterval = 5000
  private heartbeatInterval: number | null = null
  private messageHandlers = new Map<string, Function[]>()

  // Reactive state
  public isConnected = ref(false)
  public connectionError = ref<string | null>(null)
  public lastMessage = ref<WebSocketMessage | null>(null)

  // Real-time data streams
  public prices = reactive(new Map<string, PriceUpdate>())
  public trades = ref<TradeUpdate[]>([])
  public payments = ref<PaymentUpdate[]>([])
  public notifications = ref<any[]>([])

  constructor() {
    this.setupEventHandlers()
  }

  private setupEventHandlers() {
    // Price updates
    this.on('price_update', (data: PriceUpdate) => {
      this.prices.set(data.symbol, data)
    })

    // Trade updates
    this.on('trade_update', (data: TradeUpdate) => {
      const existingIndex = this.trades.value.findIndex(t => t.id === data.id)
      if (existingIndex >= 0) {
        this.trades.value[existingIndex] = data
      } else {
        this.trades.value.unshift(data)
        // Keep only last 100 trades
        if (this.trades.value.length > 100) {
          this.trades.value.pop()
        }
      }
    })

    // Payment updates
    this.on('payment_update', (data: PaymentUpdate) => {
      const existingIndex = this.payments.value.findIndex(p => p.id === data.id)
      if (existingIndex >= 0) {
        this.payments.value[existingIndex] = data
      } else {
        this.payments.value.unshift(data)
        // Keep only last 50 payments
        if (this.payments.value.length > 50) {
          this.payments.value.pop()
        }
      }
    })

    // Notifications
    this.on('notification', (data: any) => {
      this.notifications.value.unshift(data)
      // Keep only last 20 notifications
      if (this.notifications.value.length > 20) {
        this.notifications.value.pop()
      }
    })

    // System events
    this.on('system_alert', (data: any) => {
      console.warn('System Alert:', data)
      // Could show toast notification
    })
  }

  public connect(token?: string) {
    const wsUrl = this.getWebSocketUrl()
    const url = token ? `${wsUrl}?token=${token}` : wsUrl

    try {
      this.ws = new WebSocket(url)
      this.setupWebSocketEvents()
    } catch (error) {
      console.error('WebSocket connection failed:', error)
      this.connectionError.value = 'Failed to connect to real-time service'
    }
  }

  private getWebSocketUrl(): string {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = import.meta.env.VITE_WS_HOST || window.location.host
    return `${protocol}//${host}/ws/trading/`
  }

  private setupWebSocketEvents() {
    if (!this.ws) return

    this.ws.onopen = () => {
      console.log('WebSocket connected')
      this.isConnected.value = true
      this.connectionError.value = null
      this.reconnectAttempts = 0
      this.startHeartbeat()
    }

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data)
        this.lastMessage.value = message
        this.handleMessage(message)
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    this.ws.onclose = (event) => {
      console.log('WebSocket disconnected:', event.code, event.reason)
      this.isConnected.value = false
      this.stopHeartbeat()
      
      if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
        this.scheduleReconnect()
      }
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      this.connectionError.value = 'Connection error occurred'
    }
  }

  private handleMessage(message: WebSocketMessage) {
    const handlers = this.messageHandlers.get(message.type)
    if (handlers) {
      handlers.forEach(handler => handler(message.data))
    }
  }

  private startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.send('ping', {})
      }
    }, 30000) // 30 seconds
  }

  private stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval)
      this.heartbeatInterval = null
    }
  }

  private scheduleReconnect() {
    this.reconnectAttempts++
    const delay = this.reconnectInterval * this.reconnectAttempts
    
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`)
    
    setTimeout(() => {
      this.connect()
    }, delay)
  }

  public send(type: string, data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const message = {
        type,
        data,
        timestamp: Date.now()
      }
      this.ws.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket not connected, cannot send message:', type)
    }
  }

  public on(messageType: string, handler: Function) {
    if (!this.messageHandlers.has(messageType)) {
      this.messageHandlers.set(messageType, [])
    }
    this.messageHandlers.get(messageType)!.push(handler)
  }

  public off(messageType: string, handler: Function) {
    const handlers = this.messageHandlers.get(messageType)
    if (handlers) {
      const index = handlers.indexOf(handler)
      if (index > -1) {
        handlers.splice(index, 1)
      }
    }
  }

  public subscribe(channels: string[]) {
    this.send('subscribe', { channels })
  }

  public unsubscribe(channels: string[]) {
    this.send('unsubscribe', { channels })
  }

  public disconnect() {
    if (this.ws) {
      this.ws.close(1000, 'Client disconnect')
      this.ws = null
    }
    this.stopHeartbeat()
    this.isConnected.value = false
  }

  // Utility methods
  public getPriceForSymbol(symbol: string): PriceUpdate | null {
    return this.prices.get(symbol) || null
  }

  public getRecentTrades(limit: number = 10): TradeUpdate[] {
    return this.trades.value.slice(0, limit)
  }

  public getPendingPayments(): PaymentUpdate[] {
    return this.payments.value.filter(p => p.status === 'pending')
  }

  public clearNotifications() {
    this.notifications.value = []
  }
}

// Create singleton instance
export const wsService = new WebSocketService()

// Export reactive properties for easy use in components
export const useWebSocket = () => ({
  isConnected: wsService.isConnected,
  connectionError: wsService.connectionError,
  prices: wsService.prices,
  trades: wsService.trades,
  payments: wsService.payments,
  notifications: wsService.notifications,
  
  // Methods
  connect: wsService.connect.bind(wsService),
  disconnect: wsService.disconnect.bind(wsService),
  send: wsService.send.bind(wsService),
  subscribe: wsService.subscribe.bind(wsService),
  unsubscribe: wsService.unsubscribe.bind(wsService),
  getPriceForSymbol: wsService.getPriceForSymbol.bind(wsService),
  getRecentTrades: wsService.getRecentTrades.bind(wsService),
  getPendingPayments: wsService.getPendingPayments.bind(wsService),
  clearNotifications: wsService.clearNotifications.bind(wsService)
})

export default wsService