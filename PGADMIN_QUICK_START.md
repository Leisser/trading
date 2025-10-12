# 🚀 pgAdmin Quick Start Guide

## 🌐 **Access pgAdmin**

### **URL:** http://localhost:5050

**Status:** ✅ Running on port 5050

---

## 🔑 **Login Credentials**

```
Email:    admin@fluxor.pro
Password: admin123
```

---

## 📊 **Add Database Connection**

### **Method 1: Quick Setup**

1. Open http://localhost:5050
2. Login with credentials above
3. Right-click **"Servers"** → **"Register"** → **"Server"**
4. Fill in the following:

#### **General Tab:**
```
Name: Fluxor Trading Database
```

#### **Connection Tab:**
```
Host:     db
Port:     5432
Database: fluxor_api
Username: postgres
Password: postgres
```

5. Check **"Save password"**
6. Click **"Save"**

---

## 🔍 **Important Tables to Explore**

### **👤 User Tables**
| Table | Description |
|-------|-------------|
| `accounts_user` | All users (2 users currently) |
| `user_sessions` | Active login sessions |

### **💰 Wallet Tables**
| Table | Description |
|-------|-------------|
| `wallets_wallet` | User wallet (legacy) |
| `wallets_multicurrencywallet` | Multi-currency wallets |
| `wallets_cryptobalance` | Individual crypto balances |

### **🏦 Deposit Tables**
| Table | Description |
|-------|-------------|
| `trades_depositwallet` | System deposit addresses (5 created) |
| `trades_userdepositrequest` | User deposit requests |

### **📈 Trading Tables**
| Table | Description |
|-------|-------------|
| `trades_trade` | Trade history (0 trades currently) |
| `trades_cryptocurrency` | Available cryptocurrencies (5 active) |

---

## 💡 **Useful SQL Queries**

### **1. View All Users and Their Balances**
```sql
SELECT 
    u.id,
    u.email,
    u.username,
    mcw.wallet_address,
    mcw.is_active as wallet_active,
    u.date_joined as registered
FROM accounts_user u
LEFT JOIN wallets_multicurrencywallet mcw ON u.id = mcw.user_id
ORDER BY u.id;
```

### **2. View User Crypto Balances**
```sql
SELECT 
    u.email,
    c.symbol,
    c.name,
    cb.balance,
    c.current_price,
    (cb.balance * c.current_price) as usd_value
FROM wallets_cryptobalance cb
JOIN wallets_multicurrencywallet mcw ON cb.wallet_id = mcw.id
JOIN accounts_user u ON mcw.user_id = u.id
JOIN trades_cryptocurrency c ON cb.cryptocurrency_id = c.id
ORDER BY u.email, c.symbol;
```

### **3. View All Deposit Wallets**
```sql
SELECT 
    dw.id,
    c.symbol,
    c.name,
    dw.wallet_address,
    dw.wallet_name,
    dw.is_active,
    dw.is_primary,
    dw.current_balance,
    dw.min_confirmation_blocks
FROM trades_depositwallet dw
JOIN trades_cryptocurrency c ON dw.cryptocurrency_id = c.id
ORDER BY c.symbol;
```

### **4. View Trade History**
```sql
SELECT 
    t.id,
    u.email,
    c.symbol,
    t.trade_type,
    t.amount,
    t.price,
    t.total_value,
    t.leverage,
    t.status,
    t.pnl as profit_loss,
    t.created_at
FROM trades_trade t
JOIN accounts_user u ON t.user_id = u.id
JOIN trades_cryptocurrency c ON t.cryptocurrency_id = c.id
ORDER BY t.created_at DESC
LIMIT 20;
```

### **5. View User Sessions**
```sql
SELECT 
    s.id,
    u.email,
    s.created_at,
    s.expires_at,
    s.last_used_at,
    s.ip_address,
    s.is_active
FROM user_sessions s
JOIN accounts_user u ON s.user_id = u.id
WHERE s.is_active = true
ORDER BY s.created_at DESC;
```

### **6. Check Total Balance by User**
```sql
SELECT 
    u.email,
    u.username,
    COUNT(cb.id) as num_assets,
    SUM(cb.balance * c.current_price) as total_usd_balance
FROM accounts_user u
LEFT JOIN wallets_multicurrencywallet mcw ON u.id = mcw.user_id
LEFT JOIN wallets_cryptobalance cb ON mcw.id = cb.wallet_id
LEFT JOIN trades_cryptocurrency c ON cb.cryptocurrency_id = c.id
GROUP BY u.id, u.email, u.username
ORDER BY total_usd_balance DESC NULLS LAST;
```

---

## 🛠️ **Quick Database Actions**

### **Add Balance to User (via SQL)**
```sql
-- Get user's wallet ID
SELECT id, wallet_address FROM wallets_multicurrencywallet WHERE user_id = 2;

-- Get USDT cryptocurrency ID
SELECT id, symbol, current_price FROM trades_cryptocurrency WHERE symbol = 'USDT';

-- Insert or update balance
INSERT INTO wallets_cryptobalance (wallet_id, cryptocurrency_id, balance, total_deposited, created_at, updated_at)
VALUES (1, 1, 10000, 10000, NOW(), NOW())
ON CONFLICT (wallet_id, cryptocurrency_id) 
DO UPDATE SET 
    balance = wallets_cryptobalance.balance + 10000,
    total_deposited = wallets_cryptobalance.total_deposited + 10000,
    updated_at = NOW();
```

### **View Current System Status**
```sql
SELECT 
    'Total Users' as metric, 
    COUNT(*)::text as value 
FROM accounts_user
UNION ALL
SELECT 
    'Active Wallets', 
    COUNT(*)::text 
FROM wallets_multicurrencywallet WHERE is_active = true
UNION ALL
SELECT 
    'Deposit Wallets', 
    COUNT(*)::text 
FROM trades_depositwallet WHERE is_active = true
UNION ALL
SELECT 
    'Total Trades', 
    COUNT(*)::text 
FROM trades_trade
UNION ALL
SELECT 
    'Active Cryptocurrencies', 
    COUNT(*)::text 
FROM trades_cryptocurrency WHERE is_active = true;
```

---

## 📱 **Current Database State**

### **Users:** 2
- admin@fluxor.pro (ID: 1)
- enoch.mbuga@gmail.com (ID: 2)

### **Wallets:** 
- 1 Legacy Wallet
- 1 Multi-Currency Wallet (MCW_A2DC1D58CFD14735)

### **Deposit Wallets:** 5
- BTC, ETH, USDT, BNB, SOL

### **Crypto Balances:** 0
- User wallet is empty (needs funding)

### **Trades:** 0
- No trades executed yet

---

## 🎯 **Next Steps**

1. **Login to pgAdmin:** http://localhost:5050
2. **Add database connection** using credentials above
3. **Run queries** to explore data
4. **Add test balance** using the SQL query above
5. **Monitor trades** as they execute

---

## 🔧 **Advanced Features**

### **Export Data**
1. Right-click table → **"Import/Export"**
2. Choose format (CSV, JSON, etc.)
3. Set options and export

### **Backup Database**
```bash
docker-compose exec db pg_dump -U postgres fluxor_api > backup_$(date +%Y%m%d).sql
```

### **Execute Python in Database Context**
```bash
docker-compose exec api python manage.py shell
```

---

## 🚨 **Security Notes**

⚠️ **For Development Only:**
- Default credentials should be changed in production
- Database is exposed on localhost:5432
- pgAdmin is exposed on localhost:5050

✅ **For Production:**
- Use strong passwords
- Enable SSL connections
- Restrict network access
- Use environment variables
- Enable authentication

---

## 💡 **Tips & Tricks**

1. **Refresh Data:** Press `F5` or right-click → Refresh
2. **Query Tool:** Select database → Tools → Query Tool
3. **Table Data:** Right-click table → View/Edit Data → All Rows
4. **ERD Diagram:** Right-click database → ERD For Database
5. **Search:** Use the search box in the object browser

---

✅ **pgAdmin is ready at http://localhost:5050**

**Start exploring your trading platform database!** 🚀

