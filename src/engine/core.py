import pandas as pd
import numpy as np
import yfinance as yf
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class TradingEngine:
    def __init__(self):
        self.portfolio = {}
        self.historical_data = {}
        self.risk_parameters = {
            'max_position_size': 0.1,  # 10% of portfolio
            'max_drawdown': 0.2,       # 20% max drawdown
            'stop_loss': 0.05,         # 5% stop loss
            'take_profit': 0.1         # 10% take profit
        }
    
    def fetch_market_data(self, symbols: List[str], start_date: str, end_date: str) -> Dict[str, pd.DataFrame]:
        """Fetch historical market data for given symbols"""
        data = {}
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                df = ticker.history(start=start_date, end=end_date)
                data[symbol] = df
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
        return data
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators for trading signals"""
        df = data.copy()
        
        # Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        return df
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on technical indicators"""
        df = data.copy()
        
        # Initialize signal column
        df['Signal'] = 0
        
        # Buy signals
        df.loc[(df['SMA_20'] > df['SMA_50']) & 
               (df['RSI'] < 30) & 
               (df['MACD'] > df['Signal_Line']), 'Signal'] = 1
        
        # Sell signals
        df.loc[(df['SMA_20'] < df['SMA_50']) & 
               (df['RSI'] > 70) & 
               (df['MACD'] < df['Signal_Line']), 'Signal'] = -1
        
        return df
    
    def calculate_position_size(self, symbol: str, price: float, portfolio_value: float) -> float:
        """Calculate position size based on risk parameters"""
        max_position_value = portfolio_value * self.risk_parameters['max_position_size']
        return max_position_value / price
    
    def execute_trade(self, symbol: str, signal: int, price: float, portfolio_value: float) -> Dict:
        """Execute a trade based on the signal"""
        position_size = self.calculate_position_size(symbol, price, portfolio_value)
        
        if signal == 1:  # Buy
            return {
                'action': 'BUY',
                'symbol': symbol,
                'quantity': position_size,
                'price': price,
                'timestamp': datetime.now().isoformat()
            }
        elif signal == -1:  # Sell
            return {
                'action': 'SELL',
                'symbol': symbol,
                'quantity': position_size,
                'price': price,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'action': 'HOLD',
                'symbol': symbol,
                'timestamp': datetime.now().isoformat()
            }
    
    def update_portfolio(self, trade: Dict):
        """Update portfolio with new trade"""
        symbol = trade['symbol']
        if trade['action'] == 'BUY':
            self.portfolio[symbol] = {
                'quantity': trade['quantity'],
                'entry_price': trade['price'],
                'entry_time': trade['timestamp']
            }
        elif trade['action'] == 'SELL':
            if symbol in self.portfolio:
                del self.portfolio[symbol]
    
    def calculate_portfolio_value(self) -> float:
        """Calculate current portfolio value"""
        total_value = 0
        for symbol, position in self.portfolio.items():
            try:
                current_price = yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1]
                total_value += position['quantity'] * current_price
            except Exception as e:
                print(f"Error calculating value for {symbol}: {str(e)}")
        return total_value 