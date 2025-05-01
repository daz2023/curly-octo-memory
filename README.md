# AI Hedge Fund

An AI-powered hedge fund application that uses machine learning and technical analysis to make trading decisions.

## Features

- Real-time market data analysis
- Technical indicators calculation (SMA, RSI, MACD)
- Automated trading signals
- Risk management
- Portfolio tracking
- Lambda function integration
- Supabase database integration

## Project Structure

```
.
├── src/
│   ├── engine/
│   │   └── core.py           # Core trading engine
│   ├── lambda/
│   │   └── trading_handler.py # AWS Lambda handler
│   └── database/
│       └── supabase.py       # Database operations
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export SUPABASE_URL=your_supabase_url
export SUPABASE_KEY=your_supabase_key
export TRADING_SYMBOLS=AAPL,MSFT,GOOGL
```

3. Deploy Lambda function:
```bash
# Package the function
zip -r function.zip src/ lambda_function.py

# Deploy to AWS Lambda
aws lambda create-function \
    --function-name trading-engine \
    --runtime python3.9 \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --role arn:aws:iam::account-id:role/lambda-role
```

## Trading Strategy

The trading engine uses a combination of technical indicators to generate trading signals:

1. Moving Averages (SMA 20 and 50)
2. Relative Strength Index (RSI)
3. Moving Average Convergence Divergence (MACD)

Buy signals are generated when:
- SMA 20 crosses above SMA 50
- RSI is below 30 (oversold)
- MACD crosses above signal line

Sell signals are generated when:
- SMA 20 crosses below SMA 50
- RSI is above 70 (overbought)
- MACD crosses below signal line

## Risk Management

The system implements several risk management features:
- Maximum position size (10% of portfolio)
- Maximum drawdown (20%)
- Stop loss (5%)
- Take profit (10%)

## Database Schema

The Supabase database stores:
- User accounts
- Trading history
- Portfolio positions
- Performance metrics

## License

MIT License 