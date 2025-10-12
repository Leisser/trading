# PgAdmin Database Management

## 🌐 Access PgAdmin

**URL**: http://localhost:5050

---

## 🔑 Login Credentials

```
Email: admin@fluxor.pro
Password: admin123
```

---

## 📁 Add Database Server

After logging in, add a new server connection:

### Step 1: Right-click "Servers" → Register → Server

### Step 2: General Tab
```
Name: Fluxor Database
```

### Step 3: Connection Tab
```
Host name/address: db
Port: 5432
Maintenance database: fluxor_api
Username: postgres
Password: postgres
```

### Step 4: Advanced Tab (Optional)
```
DB restriction: fluxor_api
```

### Step 5: Click "Save"

---

## 📊 Database Information

| Setting | Value |
|---------|-------|
| **Host** | `db` (Docker container name) |
| **Port** | `5432` |
| **Database** | `fluxor_api` |
| **Username** | `postgres` |
| **Password** | `postgres` |

---

## 🔍 View Your Data

Once connected, you can explore:

### User Tables
- **accounts_user** - User accounts (includes Firebase users!)
- **accounts_usersession** - Active sessions
- **accounts_verificationdocument** - KYC documents

### Wallet Tables
- **wallets_wallet** - User wallets
- **wallets_cryptocurrency** - Supported cryptocurrencies

### Trading Tables
- **trades_trade** - Trade history
- **trades_deposit** - Deposit transactions
- **trades_withdrawal** - Withdrawal transactions

### Firebase User Data
Look in `accounts_user` table for:
- `firebase_uid` - Firebase user ID
- `auth_provider` - 'firebase'
- `email_verified` - Verification status
- `avatar` - Photo URL from OAuth

---

## 🛠️ Useful SQL Queries

### View All Firebase Users
```sql
SELECT 
    id,
    username,
    email,
    full_name,
    firebase_uid,
    auth_provider,
    email_verified,
    created_at
FROM accounts_user
WHERE auth_provider = 'firebase'
ORDER BY created_at DESC;
```

### View Active Sessions
```sql
SELECT 
    s.id,
    u.email,
    u.full_name,
    s.created_at,
    s.expires_at,
    s.is_active
FROM accounts_usersession s
JOIN accounts_user u ON s.user_id = u.id
WHERE s.is_active = true
ORDER BY s.created_at DESC;
```

### View Recent Trades
```sql
SELECT 
    t.id,
    u.email,
    t.cryptocurrency_symbol,
    t.trade_type,
    t.amount,
    t.price,
    t.status,
    t.created_at
FROM trades_trade t
JOIN accounts_user u ON t.user_id = u.id
ORDER BY t.created_at DESC
LIMIT 20;
```

---

## 🔧 Quick Actions

### Backup Database
```bash
docker-compose exec db pg_dump -U postgres fluxor_api > backup.sql
```

### Restore Database
```bash
docker-compose exec -T db psql -U postgres fluxor_api < backup.sql
```

### Access Database via Terminal
```bash
docker-compose exec db psql -U postgres -d fluxor_api
```

---

## 📊 Current Users

After your Firebase authentication test, you should see:
- **enoch.mbuga@gmail.com** - Auto-created via Google OAuth
- Any other test users you created

---

## 💡 Tips

1. **Refresh Data**: Use F5 or right-click → Refresh
2. **Export Data**: Right-click table → Import/Export
3. **Run Queries**: Tools → Query Tool
4. **View Logs**: Right-click connection → View Logs

---

## 🚨 Important Notes

⚠️ **Production Warning**: 
- Change default PgAdmin password
- Use strong database passwords
- Restrict access with firewall rules
- Enable SSL connections

✅ **Development**: Current settings are fine for local development

---

**PgAdmin is ready!** Open http://localhost:5050 and start exploring your data! 🎯

