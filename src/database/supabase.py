from supabase import create_client, Client
from typing import Dict, List, Optional
from datetime import datetime
from ..config import SUPABASE_URL, SUPABASE_KEY

class Database:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def create_user(self, email: str, password: str, name: str) -> Dict:
        """Create a new user account"""
        try:
            response = self.supabase.auth.sign_up({
                'email': email,
                'password': password
            })
            
            # Create user profile
            self.supabase.table('profiles').insert({
                'id': response.user.id,
                'name': name,
                'email': email,
                'created_at': datetime.now().isoformat()
            }).execute()
            
            return {
                'success': True,
                'user_id': response.user.id
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def login(self, email: str, password: str) -> Dict:
        """Authenticate user"""
        try:
            response = self.supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            return {
                'success': True,
                'session': response.session
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_trade(self, user_id: str, trade_data: Dict) -> Dict:
        """Save trade information"""
        try:
            response = self.supabase.table('trades').insert({
                'user_id': user_id,
                'symbol': trade_data['symbol'],
                'action': trade_data['action'],
                'quantity': trade_data.get('quantity'),
                'price': trade_data['price'],
                'timestamp': trade_data['timestamp'],
                'indicators': trade_data.get('indicators', {})
            }).execute()
            
            return {
                'success': True,
                'trade_id': response.data[0]['id']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_portfolio(self, user_id: str) -> Dict:
        """Get user's current portfolio"""
        try:
            response = self.supabase.table('portfolios').select('*').eq('user_id', user_id).execute()
            return {
                'success': True,
                'portfolio': response.data
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_portfolio(self, user_id: str, portfolio_data: Dict) -> Dict:
        """Update user's portfolio"""
        try:
            response = self.supabase.table('portfolios').upsert({
                'user_id': user_id,
                'positions': portfolio_data,
                'updated_at': datetime.now().isoformat()
            }).execute()
            
            return {
                'success': True,
                'portfolio': response.data
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_trading_history(self, user_id: str, limit: int = 100) -> Dict:
        """Get user's trading history"""
        try:
            response = self.supabase.table('trades').select('*').eq('user_id', user_id).order('timestamp', desc=True).limit(limit).execute()
            return {
                'success': True,
                'trades': response.data
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_performance_metrics(self, user_id: str) -> Dict:
        """Calculate and return performance metrics"""
        try:
            # Get all trades
            trades = self.get_trading_history(user_id, limit=1000)
            if not trades['success']:
                return trades
            
            # Calculate metrics
            total_trades = len(trades['trades'])
            winning_trades = sum(1 for trade in trades['trades'] if trade['action'] == 'SELL' and trade['price'] > trade['entry_price'])
            win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
            
            # Get portfolio value
            portfolio = self.get_portfolio(user_id)
            if not portfolio['success']:
                return portfolio
            
            current_value = sum(position['quantity'] * position['current_price'] for position in portfolio['portfolio'])
            
            return {
                'success': True,
                'metrics': {
                    'total_trades': total_trades,
                    'win_rate': win_rate,
                    'current_portfolio_value': current_value
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 