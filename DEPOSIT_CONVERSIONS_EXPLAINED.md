# 💰 Deposit Conversions Explained

## 📊 **Overview**

The deposit system handles cryptocurrency deposits and tracks them in both **native currency** (BTC, ETH, etc.) and **USD equivalent**. Here's how conversions work:

---

## 🔄 **Key Concepts**

### **1. No Automatic Currency Conversion**
- **Deposits stay in original cryptocurrency**
- User deposits BTC → Balance shows BTC (not converted to USD/USDT)
- User deposits USDT → Balance shows USDT
- **No conversion fees** because there's no actual conversion

### **2. USD Value Calculation**
- Each cryptocurrency has a `current_price` in USD
- Total balance USD = Sum of (crypto_amount × crypto_price)
- **Dynamic calculation** - updates with price changes

---

## 💸 **Deposit Flow**

### **Step 1: User Makes Deposit Request**

```
User sends: 0.5 BTC
To address: bc1qaf4070ccd5aae6ecfcf3d24b329c56dd8f4aae43
Transaction: 0x123abc...
```

**Creates:** `UserDepositRequest`
```python
{
  "user": "enoch.mbuga@gmail.com",
  "deposit_wallet": DepositWallet(BTC),
  "amount": 0.5,  # In BTC
  "cryptocurrency": Bitcoin,
  "transaction_hash": "0x123abc...",
  "status": "pending"
}
```

---

### **Step 2: Admin Approves Deposit**

Admin clicks "Approve" on board page → Triggers approval process:

```python
# 1. Create Deposit record
Deposit.objects.create(
    user=user,
    amount=0.5,  # BTC amount
    cryptocurrency=Bitcoin,
    status='confirmed'
)

# 2. Credit user's multi-currency wallet
crypto_balance.balance += 0.5  # Add 0.5 BTC
crypto_balance.total_deposited += 0.5
```

**Result:** User gets **0.5 BTC** in their wallet

---

### **Step 3: Balance Display & Conversion**

#### **Multi-Currency Balance:**
```python
CryptoBalance:
  cryptocurrency: Bitcoin (BTC)
  balance: 0.5
  current_price: $28,663.51
  
USD Value = 0.5 × $28,663.51 = $14,331.76
```

#### **Total Balance Calculation:**
```python
def get_total_balance_usd(self):
    total = Decimal('0')
    balances = CryptoBalance.objects.filter(wallet=self)
    
    for balance in balances:
        # Calculate USD value for each crypto
        usd_value = balance.balance × balance.cryptocurrency.current_price
        total += usd_value
    
    return total
```

---

## 📈 **Example: Multiple Deposits**

### **Scenario:**
User makes 3 deposits:
1. 0.5 BTC
2. 5 ETH  
3. 10,000 USDT

### **Storage (No Conversion):**
```
CryptoBalance Table:
┌─────────┬──────────┬───────────────┬────────────────┐
│ Symbol  │ Balance  │ Current Price │ USD Value      │
├─────────┼──────────┼───────────────┼────────────────┤
│ BTC     │ 0.5      │ $28,663.51    │ $14,331.76     │
│ ETH     │ 5.0      │ $3,247.79     │ $16,238.95     │
│ USDT    │ 10,000   │ $1.00         │ $10,000.00     │
└─────────┴──────────┴───────────────┴────────────────┘

Total USD Balance: $40,570.71
```

### **Key Points:**
✅ **No conversion** - Each crypto stays separate
✅ **Dynamic USD value** - Changes with market prices
✅ **Multi-currency** - User holds all 3 cryptos simultaneously

---

## 🔀 **When Conversion Actually Happens**

### **1. Trading (Buy/Sell)**
```python
# User buys BTC with USDT
execute_buy_order('BTC', amount=0.1, price=28663.51)

# What happens:
USDT Balance: 10,000 → 7,133.65  # Deduct $2,866.35
BTC Balance:  0.5 → 0.6           # Add 0.1 BTC
```

### **2. Swapping**
```python
# User swaps ETH → BTC
execute_swap(from='ETH', to='BTC', amount=1.0)

# Conversion logic:
ETH: 1.0 ETH × $3,247.79 = $3,247.79 USD value
BTC: $3,247.79 ÷ $28,663.51 = 0.1133 BTC
Fee: 0.3% = 0.00034 BTC
User gets: 0.11296 BTC

# Final balances:
ETH: 5.0 → 4.0    # Deduct 1 ETH
BTC: 0.5 → 0.613  # Add 0.113 BTC (after fee)
```

---

## 💱 **Conversion Rate Calculation**

### **Formula:**
```
USD Value = Crypto Amount × Current Price
```

### **Example:**
```python
# Bitcoin
amount = 0.5 BTC
price = $28,663.51
usd_value = 0.5 × 28,663.51 = $14,331.76

# Ethereum
amount = 5 ETH
price = $3,247.79
usd_value = 5 × 3,247.79 = $16,238.95

# USDT (Stablecoin)
amount = 10,000 USDT
price = $1.00
usd_value = 10,000 × 1.00 = $10,000.00
```

---

## 🏦 **Legacy Wallet Update**

For backward compatibility, deposits also update the old `Wallet` model:

```python
# Legacy wallet stores approximate USD value
wallet.balance += deposit.amount  # Adds crypto amount
wallet.save()
```

**Note:** This is **not a conversion** - it's just for compatibility with older code. The multi-currency wallet is the source of truth.

---

## 📊 **Balance Display Logic**

### **Frontend Display:**
```typescript
// API returns total USD balance
GET /api/balance/
Response: {
  "balance": 72799.06,
  "total_balance_usd": 72799.06
}

// Display on UI
<p>Available Balance</p>
<p>${userBalance.toLocaleString()}</p>
// Shows: $72,799.06
```

### **Backend Calculation:**
```python
# Multi-currency wallet method
def get_total_balance_usd(self):
    balances = CryptoBalance.objects.filter(wallet=self)
    return sum(b.balance * b.cryptocurrency.current_price 
               for b in balances)
```

---

## 🎯 **Real-World Example**

### **User Story:**
1. **User deposits 0.5 BTC** to deposit address
2. **Admin approves** → User gets 0.5 BTC
3. **Price changes** from $28,663 → $30,000
4. **Balance updates dynamically:**
   - BTC amount: **0.5** (unchanged)
   - USD value: **$15,000** (was $14,332)

### **Key Insight:**
```
✅ Crypto amount stays constant: 0.5 BTC
✅ USD value changes with price: $14,332 → $15,000
✅ No conversion needed - just calculation
```

---

## 🔐 **Deposit Wallet Statistics**

Each deposit wallet tracks totals:

```python
DepositWallet:
  cryptocurrency: Bitcoin
  wallet_address: bc1qaf4070...
  current_balance: 0.5 BTC
  total_received: 2.5 BTC    # All-time total
  total_confirmed: 2.5 BTC   # Confirmed amount
```

---

## 💡 **Summary**

### **✅ What Happens:**
1. User deposits **native cryptocurrency** (BTC, ETH, etc.)
2. Balance stored in **original currency**
3. USD value **calculated dynamically**
4. No conversion unless trading/swapping

### **❌ What Doesn't Happen:**
1. ❌ Auto-convert to USD/USDT
2. ❌ Conversion fees on deposit
3. ❌ Loss of crypto when depositing
4. ❌ Fixed USD value

### **🎯 Benefits:**
- ✅ **No conversion fees** on deposits
- ✅ **Hold multiple cryptos** simultaneously
- ✅ **Benefit from price increases** in any crypto
- ✅ **Flexible trading** between any pair
- ✅ **Accurate USD tracking** for reporting

---

## 📋 **Deposit Process Summary**

```
1. User Deposits
   └─> Creates UserDepositRequest
       └─> Status: pending
           └─> Amount: 0.5 BTC

2. Admin Approves
   └─> Creates Deposit record
       └─> Credits CryptoBalance
           └─> User balance: +0.5 BTC
               └─> No conversion

3. Balance Display
   └─> Calculates USD value
       └─> 0.5 BTC × $28,663.51
           └─> Shows: $14,331.76
               └─> Dynamic calculation
```

---

## 🔍 **Technical Details**

### **Database Schema:**
```sql
-- User's crypto balance (native currency)
CryptoBalance:
  wallet_id: 1
  cryptocurrency_id: 1 (BTC)
  balance: 0.500000000000  -- 8 decimal places
  total_deposited: 0.500000000000

-- Cryptocurrency prices (for conversion)
Cryptocurrency:
  id: 1
  symbol: 'BTC'
  name: 'Bitcoin'
  current_price: 28663.506706638498  -- 12 decimal places
```

### **API Endpoints:**
```
POST /api/wallets/deposit/request/
  └─> Creates deposit request

GET /api/admin/deposits/
  └─> Lists all deposits (admin)

POST /api/admin/deposits/{id}/approve/
  └─> Approves deposit (admin)

GET /api/balance/
  └─> Returns total USD balance
```

---

✅ **Deposits maintain original cryptocurrency - no conversion, just calculation!**

