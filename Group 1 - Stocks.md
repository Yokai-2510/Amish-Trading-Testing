
# Group 2: Stocks Configurations

## Overview
- Contains **4 parallel running sets**
- Each set operates **independently**
- All sets can be **individually configured**
- Sets can be **started/stopped** independently
- Contains **6 Categories or Tabs** for Customizations:
  1. Set Configuration
  2. Stocks Configurations
  3. Entry Indicators
  4. Exit Indicators
  5. Entry Conditions
  6. Exit Conditions

---

## Categories

### 1. Set Configurations
- **Set Name**
- **Set Active Toggle**
- **Broker Selection**
- **Start Time**
- **End Time**
- **Entry Conditions Refresh Interval**
- **Exit Conditions Refresh Interval**

---
### 2. Stocks Configurations
- Default Quantity for all stocks option
- Trading Instruments
  - Up to 30 stocks per set
  - Quantity can be selected for each stock.
- Collective Stocks selection (like all nifty stocks, etc)

---

### 3. Entry Indicators Configurations

#### Indicators and Configurations
1. **Bollinger Bands**
   - **Parameters**:
     - Period
     - Standard Deviation
2. **RSI**
   - **Parameters**:
     - Period
     - Overbought
     - Oversold
3. **Stochastic RSI**
   - **Parameters**: (period-k, period-d, smooth-k, smooth-d)
4. **Moving Averages**
   - **Parameters**: (period, type, source)
   - **Threshold**: -10 to 10
5. **MACD**
   - **Parameters**: (fast-period, slow-period, signal-period)
6. **ADX**
   - **Parameter**: (period)
7. **Volume**
   - **Parameter**: (threshold)
8. **Super-Trend**
   - **Parameters**: (period, multiplier)
9. **Fibonacci**
   - **Standard levels**
10. **Up Trend**
    - No. Of Candles
    - Time-Frame
    - Source (Close, Open etc.)
    - Condition (Default - Higher High)
11. **Down Trend**
    - No. Of Candles
    - Time-Frame
    - Source (Close, Open etc.)
    - Condition (Default - Lower Lows)

#### Indicators Combinations
- **Indicator Type**
- **Indicator Name**
- **Logic Gate Combination** (AND / OR)
- **Indicators Active Status** (ON / OFF)

---

### 4. Exit Indicators Configurations

#### Indicators and Configurations
1. **Bollinger Bands**
   - **Parameters**:
     - Period
     - Standard Deviation
2. **RSI**
   - **Parameters**:
     - Period
     - Overbought
     - Oversold
3. **Stochastic RSI**
   - **Parameters**: (period-k, period-d, smooth-k, smooth-d)
4. **Moving Averages**
   - **Parameters**: (period, type, source)
   - **Threshold**: -10 to 10
5. **MACD**
   - **Parameters**: (fast-period, slow-period, signal-period)
6. **ADX**
   - **Parameter**: (period)
7. **Volume**
   - **Parameter**: (threshold)
8. **Super-Trend**
   - **Parameters**: (period, multiplier)
9. **Fibonacci**
   - **Standard levels**

#### Indicators Combinations
- **Indicator Type**
- **Indicator Name**
- **Logic Gate Combination** (AND / OR)
- **Indicators Active Status** (ON / OFF)

---

### 5. Entry Configuration
- **Entry Chart Type**
  - Heiken Ashi
  - Candlestick
  - Renko
- **Entry Chart Time Frame**
- **Entry Time Exclusion**:
  - From Time
  - To Time

---

### 6. Exit Configuration
- **Exit Chart Type**
  - Heiken Ashi
  - Candlestick
  - Renko
- **Exit Chart Time Frame**

#### Stop Loss Setting
- **Stop Loss Type**
  - Price
  - Percentage
- **Stop Loss Price Value**
- **Stop Loss Percentage Value**
- **Max Stop Loss per Day**
- **Max Stop Loss per Trade**
- **Time-Based Stop Loss** (minutes)

#### Target/Profit Settings
- **Target Type**
  - Price
  - Percentage
- **Target Price Value**
- **Target Percentage Value**