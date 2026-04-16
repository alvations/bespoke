"""Portfolio and position tracking.

Flexible API:
- buy() / sell() for simple usage
- execute_trade(date, symbol, side, quantity, price) for full control
- Configurable slippage, commissions, and spread models
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Side(str, Enum):
    """Trade side."""
    BUY = "buy"
    SELL = "sell"


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
    side: str  # "buy" or "sell" or Side enum
    quantity: float
    price: float
    cost: float = 0  # commission + slippage
    commission: float = 0
    slippage: float = 0
    timestamp: Optional[str] = None
    date: Optional[Any] = None  # pd.Timestamp compatible

    @property
    def value(self) -> float:
        return self.quantity * self.price + self.cost


class Portfolio:
    """Portfolio tracker with positions, cash, and trade history.

    Compatible with both APIs:
        # bespoke style
        p = Portfolio(initial_cash=100_000)
        p.buy("AAPL", 10, 150.0)
        p.sell("AAPL", 5, 160.0)

        # full control style
        p = Portfolio(initial_cash=100_000, cash=100_000)
        p.execute_trade(date, "AAPL", Side.BUY, 10, 150.0)
    """

    def __init__(
        self,
        initial_cash: float = 100_000,
        cash: Optional[float] = None,
        positions: Optional[Dict[str, Position]] = None,
        trades: Optional[List[Trade]] = None,
        history: Optional[List[Dict]] = None,
        commission_per_trade: float = 0.0,
        slippage_pct: float = 0.0005,
        spread_model: str = "fixed",
        **kwargs,
    ):
        self.initial_cash = initial_cash
        self.cash = cash if cash is not None else initial_cash
        self.positions: Dict[str, Position] = positions if positions is not None else {}
        self.trades: List[Trade] = trades if trades is not None else []
        self.history: List[Dict[str, Any]] = history if history is not None else []
        self.snapshots: List[Dict[str, Any]] = []
        self.commission_per_trade = commission_per_trade
        self.slippage_pct = slippage_pct
        self.spread_model = spread_model
        self._volume_spreads: Dict[str, float] = kwargs.get("_volume_spreads", {})

    def buy(self, symbol: str, quantity: float, price: float) -> Trade:
        """Buy shares of a symbol."""
        slippage = price * self._get_slippage_pct(symbol)
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
            commission=self.commission_per_trade,
            slippage=quantity * slippage,
        )
        self.trades.append(trade)
        return trade

    def sell(self, symbol: str, quantity: float, price: float) -> Trade:
        """Sell shares of a symbol."""
        if symbol not in self.positions or self.positions[symbol].quantity <= 0:
            return Trade(symbol=symbol, side="sell", quantity=0, price=price)

        slippage = price * self._get_slippage_pct(symbol)
        fill_price = price - slippage
        quantity = min(quantity, self.positions[symbol].quantity)

        self.positions[symbol].sell(quantity, fill_price)
        self.cash += quantity * fill_price

        trade = Trade(
            symbol=symbol, side="sell", quantity=quantity,
            price=fill_price, cost=quantity * slippage,
            commission=self.commission_per_trade,
            slippage=quantity * slippage,
        )
        self.trades.append(trade)

        # Clean up zero positions
        if self.positions[symbol].quantity <= 0.0001:
            del self.positions[symbol]

        return trade

    def execute_trade(self, date, symbol: str, side, quantity: float, price: float) -> Trade:
        """Execute a trade — full-control API.

        Args:
            date: Trade date (pd.Timestamp or similar)
            symbol: Ticker symbol
            side: Side.BUY/Side.SELL or "buy"/"sell"
            quantity: Number of shares
            price: Execution price
        """
        side_str = side.value if isinstance(side, Side) else str(side).lower()
        if side_str == "buy":
            trade = self.buy(symbol, quantity, price)
        else:
            trade = self.sell(symbol, quantity, price)
        trade.date = date
        return trade

    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a symbol."""
        return self.positions.get(symbol)

    def total_value(self, prices: Dict[str, float]) -> float:
        """Total portfolio value (cash + positions)."""
        value = self.cash
        for sym, pos in self.positions.items():
            value += pos.market_value(prices.get(sym, pos.avg_cost))
        return value

    def snapshot(self, date, prices: Dict[str, float]) -> Dict[str, Any]:
        """Take a snapshot of portfolio state."""
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
        self.history.append(snap)
        return snap

    def final_positions(self) -> Dict[str, Dict]:
        """Get all current positions as a dict."""
        return {
            sym: {"qty": pos.quantity, "avg_cost": pos.avg_cost, "realized_pnl": pos.realized_pnl}
            for sym, pos in self.positions.items()
        }

    def set_volume_spreads(self, spreads: Dict[str, float]):
        """Set per-symbol volume-based spreads."""
        self._volume_spreads = spreads

    def _get_slippage_pct(self, symbol: str) -> float:
        """Get effective slippage for a symbol."""
        if self.spread_model == "volume" and symbol in self._volume_spreads:
            return self._volume_spreads[symbol] + self.slippage_pct
        return self.slippage_pct
