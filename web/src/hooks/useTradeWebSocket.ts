/**
 * Custom hook for trade WebSocket connection
 * Receives real-time trade_sum updates from backend
 */
import { useEffect, useRef, useState, useCallback } from 'react';
import { getWsUrl } from '@/config/api';

interface TradeUpdate {
  type: 'trade_update' | 'trade_completed' | 'balance_update' | 'connection_established' | 'pong';
  trade_id?: number;
  trade_sum?: string;
  current_price?: string;
  pnl?: string;
  status?: string;
  balance?: string;
  currency?: string;
  amount_returned?: string;
  reason?: string;
  timestamp?: string;
  message?: string;
}

interface UseTradeWebSocketReturn {
  isConnected: boolean;
  lastUpdate: TradeUpdate | null;
  reconnect: () => void;
}

export function useTradeWebSocket(): UseTradeWebSocketReturn {
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<TradeUpdate | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(`${getWsUrl()}/ws/trades/`);
      
      ws.onopen = () => {
        console.log('✅ Trade WebSocket connected');
        setIsConnected(true);
        
        // Clear any pending reconnection
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
          reconnectTimeoutRef.current = null;
        }
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📊 Trade update received:', data);
          setLastUpdate(data);
        } catch (error) {
          console.error('Failed to parse trade update:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('❌ Trade WebSocket error:', error);
      };

      ws.onclose = () => {
        console.log('🔌 Trade WebSocket disconnected');
        setIsConnected(false);
        wsRef.current = null;
        
        // Auto-reconnect after 5 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('🔄 Attempting to reconnect trade WebSocket...');
          connect();
        }, 5000);
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to connect to trade WebSocket:', error);
    }
  }, []);

  const reconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
    }
    connect();
  }, [connect]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  return {
    isConnected,
    lastUpdate,
    reconnect
  };
}

