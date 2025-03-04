## System Overview

The trading system is designed with a hierarchical structure to manage multiple trading strategies across stocks and options markets. The system is built to run multiple sets of strategies in parallel, each with its own customizable parameters.

### System Architecture

```
Trading System
├── Group 1: Stocks
│   ├── Set 1
│   ├── Set 2
│   ├── Set 3
│   └── Set 4
└── Group 2: Options
    ├── Set 1
    ├── Set 2
    ├── Set 3
    ├── Set 4
    ├── Set 5
    ├── Set 6
    ├── Set 7
    └── Set 8
```

## Hierarchical Structure

-  Groups (Top Level)
	-  Sets (Second Level)
		-  Categories (Third Level)
			- Parameters/Customization (Fourth Level)
## Set Configuration Template 

Both Group 1 and Group 2 sets will have Categories of Configurations . All categories and customizations are mostly same except the "Stocks" and "Options" Categories
#### Group 1 (Stocks ) Set Configuration Categories
  1. Set Configuration
  2. **Stocks** Configurations
  3. Entry Indicators
  4. Exit Indicators
  5. Entry Conditions
  6. Exit Conditions
#### Group 2 (Options ) Set Configuration Categories
  1. Set Configuration
  2. **Options Configurations
  3. Entry Indicators
  4. Exit Indicators
  5. Entry Conditions
  6. Exit Conditions
