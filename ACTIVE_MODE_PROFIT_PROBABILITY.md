# Active Mode Profit Probability Feature

## Overview

The trading system now includes **admin-configurable profit probability for Active Mode**. Previously, when users were actively trading, the system would always force losses. Now, admins can set a win rate percentage to give users a chance of profit even during active trading periods.

## Key Features

✅ **Configurable Win Rate in Active Mode** - Admins can set the probability of profit (0-100%)  
✅ **Separate Profit/Loss Percentages** - Different profit and loss magnitudes for active trading  
✅ **Probability-Based Outcomes** - Uses random chance to determine win/loss based on admin settings  
✅ **Default 20% Win Rate** - Balanced default that gives users occasional wins  
✅ **Backwards Compatible** - Legacy settings remain intact  

## How It Works

### Trading Modes

The system operates in two modes based on user activity:

#### 🟢 **IDLE MODE** (No Active Trading)
- **Trigger**: No trades placed in the last 10 minutes
- **Behavior**: Users ALWAYS win
- **Settings**:
  - `idle_profit_percentage`: Default 5%
  - `idle_duration_seconds`: Default 1800 (30 minutes)

#### 🔴 **ACTIVE MODE** (Users Trading)
- **Trigger**: At least one trade placed in the last 10 minutes
- **Behavior**: Probability-based wins/losses
- **Settings**:
  - `active_win_rate_percentage`: Default 20% (NEW)
  - `active_profit_percentage`: Default 10% (NEW)
  - `active_loss_percentage`: Default 80%
  - `active_duration_seconds`: Default 300 (5 minutes)

### Outcome Determination Logic

```python
# When a user places a trade in ACTIVE MODE:

1. Generate random number between 0-100
2. Compare with active_win_rate_percentage

If random_number <= active_win_rate_percentage:
    → USER WINS
    → Profit = active_profit_percentage (10%)
    → Duration = active_duration_seconds (5 minutes)
Else:
    → USER LOSES
    → Loss = active_loss_percentage (80%)
    → Duration = active_duration_seconds (5 minutes)
```

## Admin Configuration

### Django Admin Panel

1. Navigate to: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Go to: **Admin Control** → **Trading Settings**
4. Find **"ACTIVE MODE (Users Trading)"** section
5. Adjust settings:
   - **Active Win Rate %**: Probability of profit (0-100%)
   - **Active Profit %**: Profit amount when users win
   - **Active Loss %**: Loss amount when users lose
   - **Active Duration (seconds)**: How long trades stay open

### API Endpoint

**GET/PATCH** `/api/admin/settings/`

```json
{
  "is_active": true,
  
  "idle_profit_percentage": 5.00,
  "idle_duration_seconds": 1800,
  
  "active_win_rate_percentage": 20.00,
  "active_profit_percentage": 10.00,
  "active_loss_percentage": 80.00,
  "active_duration_seconds": 300
}
```

## Configuration Examples

### Conservative (Low Win Rate)
```json
{
  "active_win_rate_percentage": 10.00,
  "active_profit_percentage": 15.00,
  "active_loss_percentage": 85.00
}
```
- 10% chance of winning
- When win: 15% profit
- When lose: 85% loss

### Balanced (Default)
```json
{
  "active_win_rate_percentage": 20.00,
  "active_profit_percentage": 10.00,
  "active_loss_percentage": 80.00
}
```
- 20% chance of winning
- When win: 10% profit
- When lose: 80% loss

### Generous (High Win Rate)
```json
{
  "active_win_rate_percentage": 40.00,
  "active_profit_percentage": 8.00,
  "active_loss_percentage": 70.00
}
```
- 40% chance of winning
- When win: 8% profit
- When lose: 70% loss

### No Wins (Original Behavior)
```json
{
  "active_win_rate_percentage": 0.00,
  "active_profit_percentage": 0.00,
  "active_loss_percentage": 100.00
}
```
- 0% chance of winning
- Always lose 100%

### Always Win (Testing)
```json
{
  "active_win_rate_percentage": 100.00,
  "active_profit_percentage": 50.00,
  "active_loss_percentage": 0.00
}
```
- 100% chance of winning
- Always win 50%

## Database Schema

### New Fields in `TradingSettings` Model

```python
class TradingSettings(models.Model):
    # ACTIVE MODE - NEW FIELDS
    active_win_rate_percentage = DecimalField(
        default=20.00,
        help_text="Probability of profit in active mode (0-100%)"
    )
    
    active_profit_percentage = DecimalField(
        default=10.00,
        help_text="Profit % when users win in active mode"
    )
    
    active_loss_percentage = DecimalField(
        default=80.00,
        help_text="Loss % when users lose in active mode"
    )
```

### Migration Applied

Migration file: `admin_control/migrations/0004_add_active_mode_profit_probability.py`

## Technical Implementation

### Files Modified

1. **`admin_control/models.py`**
   - Added `active_win_rate_percentage` field
   - Added `active_profit_percentage` field
   - Updated `get_active_settings()` defaults
   - Updated `set_to_default()` method

2. **`trades/biased_trade_executor.py`**
   - Updated `determine_trade_outcome()` logic
   - Implemented probability-based outcome selection
   - Uses `random.uniform(0, 100)` for chance calculation

3. **`admin_control/admin.py`**
   - Reorganized admin interface with mode sections
   - Added emoji indicators (🟢 IDLE, 🔴 ACTIVE)
   - Updated list_display to show new fields

4. **`admin_control/serializers.py`**
   - Added new fields to API serializer
   - Added validation for win_rate_percentage (0-100)
   - Organized fields by mode

### Code Logic

```python
def determine_trade_outcome(self):
    is_active = TradingSettings.is_user_actively_trading()
    
    if is_active:
        # ACTIVE MODE: Probability-based
        random_chance = random.uniform(0, 100)
        
        if random_chance <= float(self.settings.active_win_rate_percentage):
            outcome = 'win'
            percentage = self.settings.active_profit_percentage
        else:
            outcome = 'loss'
            percentage = self.settings.active_loss_percentage
        
        duration_seconds = self.settings.active_duration_seconds
    else:
        # IDLE MODE: Always win
        outcome = 'win'
        percentage = self.settings.idle_profit_percentage
        duration_seconds = self.settings.idle_duration_seconds
    
    return (outcome, percentage, duration_seconds)
```

## Testing

### Test Scenario 1: Verify Default Settings
```bash
# Check default active mode settings
curl http://localhost:8000/api/admin/settings/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Expected:
# active_win_rate_percentage: 20.00
# active_profit_percentage: 10.00
# active_loss_percentage: 80.00
```

### Test Scenario 2: Place Trades During Active Mode
```bash
# Place 10 trades when users are active
# Expected: ~2 wins (20%), ~8 losses (80%)

for i in {1..10}; do
  curl -X POST http://localhost:8000/api/trading/execute/ \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "trade_type": "buy",
      "cryptocurrency": "BTC",
      "amount": "0.01",
      "price": "43000",
      "leverage": 1
    }'
  sleep 2
done
```

### Test Scenario 3: Modify Win Rate
```bash
# Set win rate to 50%
curl -X PATCH http://localhost:8000/api/admin/settings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "active_win_rate_percentage": 50.00
  }'

# Place trades and verify ~50% win rate
```

## User Experience

### Before (No Profit in Active Mode)
- Users actively trading: 100% loss rate
- Discouraging for active traders
- Predictable outcomes

### After (Configurable Profit Probability)
- Users actively trading: 20% win rate (default)
- Occasional wins keep users engaged
- Unpredictable outcomes create excitement
- Admin can adjust based on platform goals

## Best Practices

### Recommended Settings for Different Goals

**🎯 User Retention (Keep Users Happy)**
```
active_win_rate_percentage: 30-40%
active_profit_percentage: 8-12%
active_loss_percentage: 70-80%
```

**💰 Platform Profitability (Maximize Revenue)**
```
active_win_rate_percentage: 10-20%
active_profit_percentage: 5-10%
active_loss_percentage: 80-90%
```

**⚖️ Balanced (Default)**
```
active_win_rate_percentage: 20%
active_profit_percentage: 10%
active_loss_percentage: 80%
```

**🧪 Testing/Demo**
```
active_win_rate_percentage: 50%
active_profit_percentage: 15%
active_loss_percentage: 70%
```

## Security Notes

⚠️ **Admin Only**: Only superusers can modify these settings  
⚠️ **Audit Trail**: All changes are logged with `updated_by` field  
⚠️ **Validation**: Win rate is validated to be between 0-100%  
⚠️ **Real-time Effect**: Changes take effect on next trade placement  

## Future Enhancements

Potential improvements for future versions:

1. **Time-based Win Rates**: Different rates for different times of day
2. **User-specific Win Rates**: VIP users get better odds
3. **Dynamic Adjustment**: Automatically adjust based on platform balance
4. **Win Streak Limits**: Prevent consecutive wins
5. **Loss Streak Protection**: Guarantee win after X losses
6. **Progressive Difficulty**: Lower win rate as user profits increase

## Conclusion

This feature provides admins with fine-grained control over user trading outcomes in active mode, allowing for a balanced approach between platform profitability and user satisfaction. The probability-based system creates a more realistic and engaging trading experience while maintaining administrative oversight.

---

**Last Updated**: October 11, 2025  
**Version**: 1.0.0  
**Status**: ✅ Implemented and Tested

