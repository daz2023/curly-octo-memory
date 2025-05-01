import json
import os
from datetime import datetime, timedelta
from engine.core import TradingEngine

def lambda_handler(event, context):
    try:
        # Initialize trading engine
        engine = TradingEngine()
        
        # Get symbols from event or environment variable
        symbols = event.get('symbols', os.environ.get('TRADING_SYMBOLS', 'AAPL,MSFT,GOOGL').split(','))
        
        # Calculate date range (last 100 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=100)
        
        # Fetch market data
        market_data = engine.fetch_market_data(
            symbols=symbols,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        # Process each symbol
        trading_signals = []
        for symbol, data in market_data.items():
            # Calculate technical indicators
            data_with_indicators = engine.calculate_technical_indicators(data)
            
            # Generate signals
            signals = engine.generate_signals(data_with_indicators)
            
            # Get latest signal
            latest_signal = signals['Signal'].iloc[-1]
            latest_price = signals['Close'].iloc[-1]
            
            # Calculate portfolio value
            portfolio_value = engine.calculate_portfolio_value()
            
            # Execute trade
            trade = engine.execute_trade(
                symbol=symbol,
                signal=latest_signal,
                price=latest_price,
                portfolio_value=portfolio_value
            )
            
            # Update portfolio
            engine.update_portfolio(trade)
            
            trading_signals.append({
                'symbol': symbol,
                'signal': trade['action'],
                'price': latest_price,
                'timestamp': trade['timestamp'],
                'indicators': {
                    'SMA_20': signals['SMA_20'].iloc[-1],
                    'SMA_50': signals['SMA_50'].iloc[-1],
                    'RSI': signals['RSI'].iloc[-1],
                    'MACD': signals['MACD'].iloc[-1],
                    'Signal_Line': signals['Signal_Line'].iloc[-1]
                }
            })
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'trading_signals': trading_signals,
                'portfolio_value': engine.calculate_portfolio_value(),
                'current_positions': engine.portfolio
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 