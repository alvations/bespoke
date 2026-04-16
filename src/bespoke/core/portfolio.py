"""Portfolio and position tracking."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Position:
    """A single stock position."""

    symbol: str
    quantity: float = 0
    avg_cost: float = 0
    realized_pnl: float = 0

    @property
    def cost_basis(self) -> float:
        return self.quantity * self.avg_cost

    def buy(self, qty: float, price: float):
        total_cost = self.quantity * self.avg_cost + qty * price
        self.quantity += qty
        self.avg_cost = total_cost / self.quantity if self.quantity > 0 else 0

    def sell(self, qty: float, price: float) -> float:
        qty = min(qty, self.quantity)
        pnl = qty * (price - self.avg_cost)
        self.realized_pnl += pnl
        self.quantity -= qty
        return pnl

    def market_value(self, price: float) -> float:
        return self.quantity * price

    def unrealized_pnl(self, price: float) -> float:
        return self.quantity * (price - self.avg_cost)


@dataclass
class Trade:
    """Record of a single trade."""

    symbol: str
    side: str  # "buy" or "sell"
    quantity: float
    price: float
    cost: float = 0  # commission + slippage
    timestamp: Optional[str] = None

    @property
    def value(self) -> float:
        return self.quantity * self.price + self.cost


class Portfolio:
    """Portfolio tracker with positions, cash, and trade history."""

    def __init__(self, initial_cash: float = 100_000, slippage_pct: float = 0.0005):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.slippage_pct = slippage_pct
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.snapshots: List[Dict[str, Any]] = []

    def buy(self, symbol: str, quantity: float, price: float) -> Trade:
        slippage = price * self.slippage_pct
        fill_price = price + slippage
        cost = quantity * fill_price

        if cost > self.cash:
            quantity = self.cash / fill_price
            cost = quantity * fill_price

        if quantity <= 0:
            return Trade(symbol=symbol, side="buy", quantity=0, price=price)

        self.cash -= cost

        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol=symbol)
        self.positions[symbol].buy(quantity, fill_price)

        trade = Trade(
            symbol=symbol, side="buy", quantity=quantity,
            price=fill_price, cost=quantity * slippage,
        )
        self.trades.append(trade)
        return trade

    def sell(self, symbol: str, quantity: float, price: float) -> Trade:
        if symbol not in self.positions or self.positions[symbol].quantity <= 0:
            return Trade(symbol=symbol, side="sell", quantity=0, price=price)

        slippage = price * self.slippage_pct
        fill_price = price - slippage
        quantity = min(quantity, self.positions[symbol].quantity)

        self.positions[symbol].sell(quantity, fill_price)
        self.cash += quantity * fill_price

        trade = Trade(
            symbol=symbol, side="sell", quantity=quantity,
            price=fill_price, cost=quantity * slippage,
        )
        self.trades.append(trade)

        # Clean up zero positions
        if self.positions[symbol].quantity <= 0.0001:
            del self.positions[symbol]

        return trade

    def total_value(self, prices: Dict[str, float]) -> float:
        value = self.cash
        for sym, pos in self.positions.items():
            value += pos.market_value(prices.get(sym, pos.avg_cost))
        return value

    def snapshot(self, date, prices: Dict[str, float]) -> Dict[str, Any]:
        snap = {
            "date": date,
            "cash": self.cash,
            "total_value": self.total_value(prices),
            "positions": {
                sym: {"qty": pos.quantity, "avg_cost": pos.avg_cost}
                for sym, pos in self.positions.items()
            },
        }
        self.snapshots.append(snap)
        return snap

    def final_positions(self) -> Dict[str, Dict]:
        return {
            sym: {"qty": pos.quantity, "avg_cost": pos.avg_cost, "realized_pnl": pos.realized_pnl}
            for sym, pos in self.positions.items()
        }
