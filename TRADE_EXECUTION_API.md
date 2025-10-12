# Trade Execution API with Balance Validation & Profit/Loss Tracking

## Overview

The trade execution system now includes:
- ✅ Balance validation before trades
- ✅ Automatic profit/loss calculation
- ✅ Multi-currency wallet updates
- ✅ Trading fees (0.1% for buy/sell, 0.3% for swaps)
- ✅ Leverage support (1x to 100x)
- ✅ Transaction atomicity (database transactions)

## New API Endpoints

### 1. Execute Trade
**POST** `/api/trading/execute/`

Execute a trade with automatic balance validation and wallet updates.

#### Buy Order Example:
```json
{
  "trade_type": "buy",
  "cryptocurrency": "BTC",
  "amount": "0.1",
  "price": "43250.50",
  "leverage": 1
}
```

#### Sell Order Example:
```json
{
  "trade_type": "sell",
  "cryptocurrency": "BTC",
  "amount": "0.1",
  "price": "45000.00",
  "leverage": 1
}
```

#### Swap Example:
```json
{
  "trade_type": "swap",
  "cryptocurrency": "BTC",
  "to_cryptocurrency": "ETH",
  "amount": "0.5"
}
```

#### Response:
```json
{
  "success": true,
  "message": "Buy order executed successfully",
  "trade": {
    "id": 123,
    "cryptocurrency": "BTC",
    "trade_type": "buy",
    "amount": "0.1",
    "price": "43250.50",
    "total_value": "4325.05",
    "leverage": 1,
    "status": "executed",
    "pnl": "0.00",
    "fees": "4.33",
    "executed_at": "2025-10-11T07:45:00Z"
  },
  "pnl": 0.0,
  "fees": 4.33
}
```

#### Error Response:
```json
{
  "error": "Insufficient balance. Required: 4325.05 USDT, Available: 1000.00 USDT"
}
```

### 2. Check Balance
**GET** `/api/trading/balance/check/?symbol=BTC`

Check available balance for a specific cryptocurrency.

#### Response:
```json
{
  "symbol": "BTC",
  "available_balance": 0.5,
  "usd_value": 21625.25
}
```

### 3. Trading History
**GET** `/api/trading/history/?limit=50&trade_type=buy`

Get trading history with profit/loss summary.

#### Query Parameters:
- `limit`: Number of trades (default: 50)
- `trade_type`: Filter by type (buy, sell, swap)

#### Response:
```json
{
  "trades": [
    {
      "id": 123,
      "cryptocurrency": "BTC",
      "trade_type": "buy",
      "amount": "0.1",
      "price": "43250.50",
      "pnl": "175.00",
      "fees": "4.33",
      "executed_at": "2025-10-11T07:45:00Z"
    }
  ],
  "total_count": 15,
  "total_pnl": 1250.75,
  "summary": {
    "total_trades": 15,
    "buy_trades": 8,
    "sell_trades": 6,
    "swap_trades": 1
  }
}
```

## How It Works

### Buy Order Flow:
1. **Validate Input**: Check cryptocurrency exists and price > 0
2. **Calculate Cost**: `total_cost = amount × price`
3. **Calculate Margin**: `required_margin = total_cost / leverage`
4. **Check Balance**: Verify USDT balance >= required_margin
5. **Execute Trade**:
   - Deduct USDT from wallet
   - Add cryptocurrency to wallet
   - Create trade record with fees (0.1%)
6. **Return Result**: Trade details with PnL and fees

### Sell Order Flow:
1. **Validate Input**: Check cryptocurrency exists and price > 0
2. **Check Balance**: Verify user has enough cryptocurrency
3. **Calculate Proceeds**: `total_proceeds = amount × price`
4. **Calculate Fees**: `fees = total_proceeds × 0.001` (0.1%)
5. **Calculate PnL**: Compare to average buy price
   - `cost_basis = amount × avg_buy_price`
   - `pnl = total_proceeds - cost_basis - fees`
6. **Execute Trade**:
   - Deduct cryptocurrency from wallet
   - Add USDT to wallet (net proceeds)
   - Create trade record with PnL
7. **Return Result**: Trade details with profit/loss

### Swap Flow:
1. **Validate Input**: Check both cryptocurrencies exist
2. **Check Balance**: Verify user has source cryptocurrency
3. **Calculate Exchange**:
   - `from_usd_value = from_amount × from_crypto_price`
   - `to_amount = from_usd_value / to_crypto_price`
   - `fees = to_amount × 0.003` (0.3%)
4. **Execute Swap**:
   - Deduct source cryptocurrency
   - Add destination cryptocurrency (minus fees)
   - Create trade record
5. **Return Result**: Swap details

## Balance Management

### Multi-Currency Wallet Structure:
```
User
└── MultiCurrencyWallet
    ├── CryptoBalance (BTC)
    │   ├── balance: 1.5
    │   ├── locked_balance: 0.2
    │   └── available_balance: 1.3 (computed)
    ├── CryptoBalance (ETH)
    │   ├── balance: 10.0
    │   └── available_balance: 10.0
    └── CryptoBalance (USDT)
        ├── balance: 50000.0
        └── available_balance: 50000.0
```

### Balance Checks:
- **Buy Orders**: Check USDT balance
- **Sell Orders**: Check cryptocurrency balance
- **Swaps**: Check source cryptocurrency balance

### Balance Updates:
All balance updates are performed within database transactions (ACID compliance).

## Profit/Loss Calculation

### For Sell Orders:
```python
# Get average buy price from previous trades
avg_buy_price = previous_buy_trades.first().price

# Calculate cost basis
cost_basis = amount × avg_buy_price

# Calculate profit/loss
pnl = (amount × sell_price) - cost_basis - fees
```

### For Buy Orders:
- Initial PnL is 0
- PnL is calculated when the position is sold

### Total PnL:
Sum of all executed trades' PnL values.

## Fees Structure

| Trade Type | Fee Rate | Description |
|------------|----------|-------------|
| Buy        | 0.1%     | Applied to total cost |
| Sell       | 0.1%     | Applied to proceeds |
| Swap       | 0.3%     | Applied to destination amount |

## Leverage Trading

### Supported Leverage:
- 1x (no leverage)
- 5x, 10x, 25x, 50x, 100x

### Margin Calculation:
```
required_margin = total_cost / leverage
```

### Example:
- Trade: Buy 0.1 BTC at $43,250
- Total Cost: $4,325
- With 10x leverage: Required margin = $432.50
- Without leverage (1x): Required margin = $4,325

### Risk:
- Higher leverage = Lower margin required
- Higher leverage = Higher risk of liquidation
- Liquidation occurs if price moves against position by (1/leverage)%

## Error Handling

### Common Errors:

1. **Insufficient Balance**:
```json
{
  "error": "Insufficient balance. Required: 4325.05 USDT, Available: 1000.00 USDT"
}
```

2. **Cryptocurrency Not Found**:
```json
{
  "error": "Cryptocurrency BTC not found"
}
```

3. **Invalid Price**:
```json
{
  "error": "Price must be greater than 0 for buy orders"
}
```

4. **Missing Fields**:
```json
{
  "error": "Missing required fields: trade_type, cryptocurrency, amount"
}
```

## Database Models

### Trade Model Fields:
- `user`: ForeignKey to User
- `cryptocurrency`: ForeignKey to Cryptocurrency
- `trade_type`: 'buy', 'sell', or 'swap'
- `amount`: Decimal (20, 8)
- `price`: Decimal (20, 8)
- `total_value`: Decimal (20, 2)
- `leverage`: Integer (default: 1)
- `status`: 'pending', 'executed', 'cancelled', 'failed'
- `pnl`: Decimal (20, 2) - **Profit/Loss**
- `fees`: Decimal (10, 8) - **Trading fees**
- `executed_at`: DateTime

### CryptoBalance Model Fields:
- `wallet`: ForeignKey to MultiCurrencyWallet
- `cryptocurrency`: ForeignKey to Cryptocurrency
- `balance`: Decimal (20, 8)
- `locked_balance`: Decimal (20, 8)
- `total_deposited`: Decimal (20, 8)
- `total_withdrawn`: Decimal (20, 8)

## Frontend Integration

### Example: Place Buy Order
```typescript
const placeBuyOrder = async (symbol: string, amount: number, price: number) => {
  try {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/trading/execute/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        trade_type: 'buy',
        cryptocurrency: symbol,
        amount: amount.toString(),
        price: price.toString(),
        leverage: 1
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      alert(`Error: ${error.error}`);
      return;
    }
    
    const data = await response.json();
    alert(`Order executed! PnL: $${data.pnl}, Fees: $${data.fees}`);
    
  } catch (error) {
    console.error('Failed to place order:', error);
  }
};
```

### Example: Check Balance Before Trade
```typescript
const checkBalanceBeforeTrade = async (symbol: string, amount: number, price: number) => {
  try {
    const token = localStorage.getItem('access_token');
    
    // Check USDT balance for buy orders
    const response = await fetch('http://localhost:8000/api/trading/balance/check/?symbol=USDT', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const data = await response.json();
    const required = amount * price;
    
    if (data.available_balance < required) {
      alert(`Insufficient balance! Required: $${required}, Available: $${data.available_balance}`);
      return false;
    }
    
    return true;
    
  } catch (error) {
    console.error('Failed to check balance:', error);
    return false;
  }
};
```

## Testing

### Test Buy Order:
```bash
curl -X POST http://localhost:8000/api/trading/execute/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "trade_type": "buy",
    "cryptocurrency": "BTC",
    "amount": "0.01",
    "price": "43250.50",
    "leverage": 1
  }'
```

### Test Balance Check:
```bash
curl -X GET "http://localhost:8000/api/trading/balance/check/?symbol=BTC" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Trading History:
```bash
curl -X GET "http://localhost:8000/api/trading/history/?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Security Features

✅ **Authentication Required**: All endpoints require valid JWT token
✅ **Balance Validation**: Cannot trade more than available balance
✅ **Transaction Safety**: Database transactions ensure atomicity
✅ **Input Validation**: All inputs are validated before execution
✅ **Decimal Precision**: Uses Decimal for financial calculations (no float errors)
✅ **User Isolation**: Users can only access their own trades and balances

## Future Enhancements

- [ ] Stop-loss automation
- [ ] Take-profit automation  
- [ ] Margin calls for leveraged positions
- [ ] Advanced order types (trailing stop, OCO)
- [ ] Real-time websocket updates
- [ ] Trading pairs management
- [ ] Market orders (current price)
- [ ] Limit orders (future execution)
- [ ] Order history with detailed analytics

