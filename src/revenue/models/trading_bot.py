"""
Trading Bot Revenue Model

Automated trading bot system.
"""

from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
import json
import os
import random

from ..base import RevenueModel, RevenueConfig, RevenueResult, RevenueStatus


@dataclass
class Trade:
    """A trade"""
    id: str
    symbol: str
    type: str  # buy, sell
    amount: float
    price: float
    pnl: float = 0.0  # Profit/Loss
    status: str = "open"  # open, closed
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class Strategy:
    """Trading strategy"""
    id: str
    name: str
    description: str
    asset_class: str  # crypto, stocks, forex
    status: str = "inactive"  # active, inactive, testing
    win_rate: float = 0.0
    total_trades: int = 0
    total_pnl: float = 0.0


class TradingBot(RevenueModel):
    """
    Trading Bot - Automated trading
    
    Revenue potential: $100-$50,000 monthly (high risk)
    """
    
    ASSETS = {
        "crypto": ["BTC", "ETH", "SOL", "AVAX", "LINK"],
        "stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
        "forex": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
    }
    
    def __init__(self, config: RevenueConfig):
        super().__init__(config)
        self.strategies: List[Strategy] = []
        self.trades: List[Trade] = []
        self.portfolio_value: float = 10000.0
        self._load_data()
    
    def _load_data(self):
        """Load existing data"""
        data_dir = "/home/workspace/personai/data/revenue"
        
        strategies_file = os.path.join(data_dir, "trading_strategies.json")
        if os.path.exists(strategies_file):
            try:
                with open(strategies_file, 'r') as f:
                    data = json.load(f)
                    for s in data.get("strategies", []):
                        ts = s.get("timestamp")
                        if ts:
                            s["timestamp"] = datetime.fromisoformat(ts)
                        self.strategies.append(Strategy(**s))
            except Exception:
                pass
        
        trades_file = os.path.join(data_dir, "trading_trades.json")
        if os.path.exists(trades_file):
            try:
                with open(trades_file, 'r') as f:
                    data = json.load(f)
                    for t in data.get("trades", []):
                        ts = t.get("timestamp")
                        if ts:
                            t["timestamp"] = datetime.fromisoformat(ts)
                        self.trades.append(Trade(**t))
            except Exception:
                pass
    
    def _save_data(self):
        """Save data"""
        data_dir = "/home/workspace/personai/data/revenue"
        os.makedirs(data_dir, exist_ok=True)
        
        strategies_file = os.path.join(data_dir, "trading_strategies.json")
        strategies_data = []
        for s in self.strategies:
            sd = vars(s)
            if sd.get("timestamp"):
                sd["timestamp"] = sd["timestamp"].isoformat()
            strategies_data.append(sd)
        with open(strategies_file, 'w') as f:
            json.dump({"strategies": strategies_data}, f, indent=2)
        
        trades_file = os.path.join(data_dir, "trading_trades.json")
        trades_data = []
        for t in self.trades:
            td = vars(t)
            if td.get("timestamp"):
                td["timestamp"] = td["timestamp"].isoformat()
            trades_data.append(td)
        with open(trades_file, 'w') as f:
            json.dump({"trades": trades_data}, f, indent=2)
    
    def initialize(self) -> bool:
        """Initialize trading bot"""
        self.status = RevenueStatus.INITIALIZING
        
        # Create default strategies
        if not self.strategies:
            default_strategies = [
                ("Momentum Crypto", "Trend following on crypto", "crypto"),
                ("Mean Reversion", "Buy dips, sell peaks", "stocks"),
                ("Breakout Strategy", "Trade breakouts", "forex"),
                ("AI Signal", "ML-based signals", "crypto"),
            ]
            
            for name, desc, asset in default_strategies:
                strategy = Strategy(
                    id=f"strat_{len(self.strategies)}",
                    name=name,
                    description=desc,
                    asset_class=asset,
                    status="inactive",
                    win_rate=0.5 + random.uniform(0, 0.2)
                )
                self.strategies.append(strategy)
        
        self._load_data()
        self.status = RevenueStatus.IDLE
        return True
    
    def create_strategy(self, name: str, description: str, asset_class: str) -> Strategy:
        """Create a new strategy"""
        strategy = Strategy(
            id=f"strat_{datetime.now().timestamp()}",
            name=name,
            description=description,
            asset_class=asset_class,
            status="testing",
            win_rate=0.5
        )
        self.strategies.append(strategy)
        return strategy
    
    def activate_strategy(self, strategy_id: str) -> bool:
        """Activate a strategy"""
        for s in self.strategies:
            if s.id == strategy_id:
                s.status = "active"
                self._save_data()
                return True
        return False
    
    def execute_trade(self, strategy_id: str, symbol: str, trade_type: str, amount: float) -> Trade:
        """Execute a trade"""
        # Simulated price
        base_prices = {
            "BTC": 50000, "ETH": 3000, "SOL": 100, "AVAX": 35, "LINK": 15,
            "AAPL": 180, "MSFT": 400, "GOOGL": 150, "AMZN": 180, "NVDA": 800,
            "EUR/USD": 1.08, "GBP/USD": 1.27, "USD/JPY": 150, "AUD/USD": 0.66
        }
        
        price = base_prices.get(symbol, 100)
        
        trade = Trade(
            id=f"trade_{datetime.now().timestamp()}",
            symbol=symbol,
            type=trade_type,
            amount=amount,
            price=price,
            status="open"
        )
        self.trades.append(trade)
        
        # Update strategy stats
        for s in self.strategies:
            if s.id == strategy_id:
                s.total_trades += 1
                break
        
        return trade
    
    def close_trade(self, trade_id: str, exit_price: float = None) -> bool:
        """Close a trade and calculate P&L"""
        for trade in self.trades:
            if trade.id == trade_id and trade.status == "open":
                if exit_price is None:
                    # Simulate exit price
                    exit_price = trade.price * (1 + random.uniform(-0.05, 0.05))
                
                if trade.type == "buy":
                    trade.pnl = (exit_price - trade.price) * trade.amount
                else:
                    trade.pnl = (trade.price - exit_price) * trade.amount
                
                trade.status = "closed"
                
                # Update portfolio
                self.portfolio_value += trade.pnl
                
                # Update strategy
                for s in self.strategies:
                    s.total_pnl += trade.pnl
                    s.total_trades += 1
                    if trade.pnl > 0:
                        s.win_rate = (s.win_rate * (s.total_trades - 1) + 1) / s.total_trades
                    else:
                        s.win_rate = (s.win_rate * (s.total_trades - 1)) / s.total_trades
                
                self._save_data()
                return True
        return False
    
    def execute(self) -> RevenueResult:
        """Execute trading cycle"""
        self.status = RevenueStatus.RUNNING
        self.execution_count += 1
        
        try:
            activities = []
            cycle_pnl = 0.0
            
            # Get active strategies
            active = [s for s in self.strategies if s.status == "active"]
            testing = [s for s in self.strategies if s.status == "testing"]
            
            # Execute trades with active strategies
            if active:
                for strategy in active:
                    # Decide whether to trade
                    if random.random() < 0.7:  # 70% chance to trade
                        asset_class = strategy.asset_class
                        symbol = random.choice(self.ASSETS[asset_class])
                        trade_type = random.choice(["buy", "sell"])
                        amount = random.uniform(0.1, 1.0)
                        
                        trade = self.execute_trade(strategy.id, symbol, trade_type, amount)
                        
                        # Sometimes close immediately (day trading)
                        if random.random() < 0.5:
                            self.close_trade(trade.id)
                            cycle_pnl += trade.pnl
                
                activities.append(f"Active strategies: {len(active)}")
            
            # Test new strategies
            if testing and random.random() < 0.3:
                strategy = random.choice(testing)
                # Activate after testing
                self.activate_strategy(strategy.id)
                activities.append(f"Activated strategy: {strategy.name}")
            
            # Close some open trades
            open_trades = [t for t in self.trades if t.status == "open"]
            if open_trades:
                for trade in open_trades[:3]:
                    if random.random() < 0.3:
                        self.close_trade(trade.id)
                        cycle_pnl += trade.pnl
            
            # Risk management - limit losses
            if cycle_pnl < -self.portfolio_value * 0.05:  # 5% daily loss limit
                cycle_pnl = -self.portfolio_value * 0.05
                activities.append("Risk limit reached - stopped trading")
            
            # Update portfolio
            self.portfolio_value += cycle_pnl
            
            result = RevenueResult(
                model="trading_bot",
                amount=cycle_pnl,
                currency="USD",
                timestamp=datetime.now(),
                details={
                    "activities": activities,
                    "active_strategies": len(active),
                    "total_strategies": len(self.strategies),
                    "open_trades": len(open_trades),
                    "closed_trades": len([t for t in self.trades if t.status == "closed"]),
                    "portfolio_value": self.portfolio_value,
                    "strategy_performance": [
                        {"name": s.name, "pnl": s.total_pnl, "win_rate": s.win_rate}
                        for s in sorted(active, key=lambda x: x.total_pnl, reverse=True)
                    ]
                },
                success=True
            )
            
            self.last_result = result
            self.save_history(result)
            self.status = RevenueStatus.IDLE
            self._save_data()
            
            return result
            
        except Exception as e:
            self.status = RevenueStatus.ERROR
            return RevenueResult(
                model="trading_bot",
                amount=0.0,
                success=False,
                error=str(e)
            )
    
    def get_status(self) -> Dict[str, Any]:
        """Get status"""
        active = [s for s in self.strategies if s.status == "active"]
        closed = [t for t in self.trades if t.status == "closed"]
        
        winning = sum(1 for t in closed if t.pnl > 0)
        
        return {
            "status": self.status.value,
            "portfolio_value": self.portfolio_value,
            "active_strategies": len(active),
            "total_strategies": len(self.strategies),
            "open_trades": len([t for t in self.trades if t.status == "open"]),
            "total_pnl": sum(t.pnl for t in closed),
            "win_rate": winning / len(closed) if closed else 0,
            "total_revenue": self.total_revenue
        }
    
    def stop(self):
        """Stop the model"""
        self.is_running = False
        self.status = RevenueStatus.STOPPED
        
        # Close all open trades
        for trade in self.trades:
            if trade.status == "open":
                self.close_trade(trade.id)
        
        self._save_data()
