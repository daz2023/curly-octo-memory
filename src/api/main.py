from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from database.supabase import Database
from engine.core import TradingEngine
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and trading engine
db = Database()
engine = TradingEngine()

# Models
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class TradeSignal(BaseModel):
    symbol: str
    action: str
    price: float
    quantity: Optional[float] = None
    indicators: Optional[dict] = None

# Routes
@app.post("/auth/register")
async def register(user: UserCreate):
    result = db.create_user(user.email, user.password, user.name)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
    return {"message": "User created successfully", "user_id": result['user_id']}

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    result = db.login(form_data.username, form_data.password)
    if not result['success']:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": result['session'].access_token, "token_type": "bearer"}

@app.get("/portfolio")
async def get_portfolio(user_id: str):
    result = db.get_portfolio(user_id)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
    return result['portfolio']

@app.post("/trade")
async def execute_trade(trade: TradeSignal, user_id: str):
    trade_data = {
        'symbol': trade.symbol,
        'action': trade.action,
        'price': trade.price,
        'quantity': trade.quantity,
        'timestamp': datetime.now().isoformat(),
        'indicators': trade.indicators
    }
    
    # Save trade
    result = db.save_trade(user_id, trade_data)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
    
    # Update portfolio
    portfolio_result = db.update_portfolio(user_id, trade_data)
    if not portfolio_result['success']:
        raise HTTPException(status_code=400, detail=portfolio_result['error'])
    
    return {"message": "Trade executed successfully", "trade_id": result['trade_id']}

@app.get("/trading-history")
async def get_trading_history(user_id: str, limit: int = 100):
    result = db.get_trading_history(user_id, limit)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
    return result['trades']

@app.get("/performance")
async def get_performance(user_id: str):
    result = db.get_performance_metrics(user_id)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
    return result['metrics']

@app.get("/market-data")
async def get_market_data(symbols: str):
    symbol_list = symbols.split(',')
    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)
    
    market_data = engine.fetch_market_data(
        symbols=symbol_list,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )
    
    return market_data 