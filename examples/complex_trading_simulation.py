import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

from jgtml.fdb_signal_quality_predictor import FDBSignalQualityPredictor
from jgtml.fdb_pattern_intelligence import FDBPatternIntelligence
from jgtml.fdb_scanner_2408 import generate_fresh_and_cache

# Import jgtpy for historical data access
try:
    from jgtpy import JGTPDSP as pds
    JGTPY_AVAILABLE = True
except ImportError:
    JGTPY_AVAILABLE = False
    print("⚠️ jgtpy not available, will use synthetic data")

class Trade:
    def __init__(self, instrument: str, direction: str, price: float, quality: float, size: float):
        self.instrument = instrument
        self.direction = direction
        self.entry_price = price
        self.quality = quality
        self.size = size
        self.open_time = datetime.now()
        self.close_time = None
        self.exit_price = None
        self.profit = 0.0
        self.reason = None

    def close(self, price: float, reason: str = "target_hit"):
        self.exit_price = price
        self.close_time = datetime.now()
        self.reason = reason
        if self.direction == 'buy':
            self.profit = (price - self.entry_price) * self.size
        else:
            self.profit = (self.entry_price - price) * self.size

class ComplexTradingSimulation:
    """Simulate a series of trades leveraging FDB ecosystem tools.

    This example ties together the **FDBPatternIntelligence** system,
    the **FDBScanner** data fetcher, and the **FDBSignalQualityPredictor**.
    It demonstrates how historical intelligence and real-time scanning can
    guide a trading loop that opens and closes positions automatically.
    """

    def __init__(self, instrument: str = 'EUR-USD', timeframe: str = 'D1', days: int = 30):
        self.instrument = instrument
        self.timeframe = timeframe
        self.days = days

        # Historical intelligence used by the predictor
        self.intelligence = FDBPatternIntelligence(data_path='samples')
        self.intelligence.load_all_pattern_intelligence()

        self.predictor = FDBSignalQualityPredictor(data_path='samples')

        self.history: List[Trade] = []
        self.active_trades: List[Trade] = []
        self.balance = 10_000.0
        self.risk_per_trade = 0.02  # 2% risk per trade
        self.max_trades = 3  # Maximum concurrent trades
        
        # Performance tracking
        self.win_count = 0
        self.loss_count = 0
        self.total_trades = 0

    def _generate_market_data(self) -> Tuple[List[float], List[float], List[float]]:
        """Get historical market data from jgtpy."""
        try:
            # Import jgtpy modules
            from jgtpy import JGTPDSP as pds
            
            # Get historical data
            df = pds.getPH(self.instrument.replace('-', '/'), self.timeframe, quote_count=self.days)
            
            # Extract OHLC data
            closes = df['Close'].values.tolist()
            highs = df['High'].values.tolist()
            lows = df['Low'].values.tolist()
            
            return closes, highs, lows
        except Exception as e:
            print(f"⚠️ Error fetching historical data: {e} -- using synthetic data.")
            # Fall back to synthetic data generation if jgtpy fails
            base = 1.0
            trend = np.cumsum(np.random.normal(0.0002, 0.001, self.days))
            t = np.arange(self.days)
            cycle = 0.005 * np.sin(2 * np.pi * t / 20)
            noise = np.random.normal(0, 0.004, self.days)
            
            closes = base + trend + cycle + noise
            highs = closes + np.abs(np.random.normal(0, 0.003, self.days))
            lows = closes - np.abs(np.random.normal(0, 0.003, self.days))
            
            return closes.tolist(), highs.tolist(), lows.tolist()

    def _calculate_position_size(self, quality_score: float) -> float:
        """Calculate position size based on quality score and risk parameters."""
        # Higher quality = larger position, up to risk limit
        quality_factor = min(1.0, quality_score / 100)
        position_size = self.balance * self.risk_per_trade * quality_factor
        return round(position_size, 2)

    def _random_signal(self):
        """Generate a random fallback signal."""
        return {
            'signal_type': random.choice(['buy', 'sell']),
            'strength': random.random(),
            'context': random.choice(['fractal_breakout', 'trend_reversal', 'momentum_spike']),
            'confidence': random.random() * 0.5  # Lower confidence for random signals
        }

    def _scan_signal(self, day_index: int, prices: List[float], dates=None):
        """Scan the market data using FDBScanner or historical data."""
        try:
            # If we're using historical data with dates
            if JGTPY_AVAILABLE and dates and day_index < len(dates):
                # Get signals for the specific date from jgtpy
                date_str = dates[day_index].strftime('%Y-%m-%d')
                signals = pds.getSignals(self.instrument.replace('-', '/'), self.timeframe, date_str)
                
                if signals and len(signals) > 0:
                    # Use the first signal from the day
                    signal = signals[0]
                    sig_type = 'buy' if signal.get('direction') == 'bull' else 'sell'
                    return {
                        'signal_type': sig_type,
                        'strength': signal.get('strength', 0.7),
                        'context': signal.get('context', 'historical'),
                        'confidence': signal.get('confidence', 0.8)
                    }
            
            # Otherwise use FDBScanner for real-time data
            df = generate_fresh_and_cache(self.instrument.replace('-', '/'), self.timeframe)
            last = df.iloc[-1]
            
            # If we have real data, use it
            if last.get('fdbb', 0) == 1:
                sig_type = 'sell'
                confidence = min(0.9, abs(last.get('ao', 0)) / 2)
            elif last.get('fdbs', 0) == 1:
                sig_type = 'buy'
                confidence = min(0.9, abs(last.get('ao', 0)) / 2)
            else:
                # Fall back to simulated signals based on price action
                if day_index >= 3:
                    # Simple trend detection
                    short_ma = sum(prices[day_index-3:day_index]) / 3
                    if prices[day_index] > short_ma * 1.005:
                        return {
                            'signal_type': 'buy',
                            'strength': 0.6,
                            'context': 'price_momentum',
                            'confidence': 0.7
                        }
                    elif prices[day_index] < short_ma * 0.995:
                        return {
                            'signal_type': 'sell',
                            'strength': 0.6,
                            'context': 'price_reversal',
                            'confidence': 0.7
                        }
                return self._random_signal()

            return {
                'signal_type': sig_type,
                'strength': abs(last.get('ao', 0)),
                'context': 'scanner_realtime',
                'confidence': confidence
            }
        except Exception as e:
            print(f"⚠️ Scanner failed: {e} -- using price-based signal.")
            # Use price-based signal instead of purely random
            if day_index >= 2 and prices[day_index] > prices[day_index-1] > prices[day_index-2]:
                return {
                    'signal_type': 'buy',
                    'strength': 0.5,
                    'context': 'price_trend',
                    'confidence': 0.6
                }
            elif day_index >= 2 and prices[day_index] < prices[day_index-1] < prices[day_index-2]:
                return {
                    'signal_type': 'sell',
                    'strength': 0.5,
                    'context': 'price_trend',
                    'confidence': 0.6
                }
            return self._random_signal()

    def _manage_risk(self, day: int, price: float, score: float):
        """Manage risk by closing underperforming trades or taking profits."""
        for trade in list(self.active_trades):
            # Calculate current profit/loss
            if trade.direction == 'buy':
                current_profit = price - trade.entry_price
            else:
                current_profit = trade.entry_price - price
            
            # Exit conditions
            exit_reason = None
            
            # Take profit at 3:1 reward-to-risk ratio
            take_profit = 0.015 * trade.quality / 50  # Scale with quality
            if current_profit > take_profit:
                exit_reason = "take_profit"
            
            # Stop loss at 1% (scaled by quality)
            stop_loss = -0.01 * (100 - trade.quality) / 50  # Lower quality = tighter stop
            if current_profit < stop_loss:
                exit_reason = "stop_loss"
                
            # Exit on signal quality deterioration
            if score < 30 and trade.quality > score + 20:
                exit_reason = "signal_deterioration"
                
            # Time-based exit (trades older than 10 days)
            if day - self.history.index(trade) > 10:
                exit_reason = "time_exit"
            
            if exit_reason:
                trade.close(price, exit_reason)
                self.balance += trade.profit
                
                # Track performance
                if trade.profit > 0:
                    self.win_count += 1
                else:
                    self.loss_count += 1
                
                self.active_trades.remove(trade)
                self.history.append(trade)
                print(f"Day {day}: CLOSE {trade.direction} at {price:.4f}, profit {trade.profit:.2f} ({exit_reason})")

    def run(self):
        # Get historical market data
        closes, highs, lows = self._generate_market_data()
        
        # Get dates if using jgtpy
        dates = None
        if JGTPY_AVAILABLE:
            try:
                df = pds.getPH(self.instrument.replace('-', '/'), self.timeframe, quote_count=self.days)
                dates = df.index.tolist()
            except Exception:
                pass
        
        for day in range(1, len(closes)):
            price = closes[day]
            high = highs[day]
            low = lows[day]
            
            # Get date for logging
            date_str = dates[day].strftime('%Y-%m-%d') if dates and day < len(dates) else f"Day {day}"
            
            # Get signal and evaluate quality
            signal = self._scan_signal(day, closes, dates)
            quality = self.predictor.evaluate_signal(self.instrument, self.timeframe, signal)
            intel = self.intelligence.evaluate_fdb_signal(
                self.instrument, 
                self.timeframe, 
                'bull' if signal['signal_type'] == 'buy' else 'bear'
            )
            
            # Combine scores with confidence weighting
            confidence = signal.get('confidence', 0.5)
            score = (quality['overall_quality_score'] * 0.4 + 
                    intel['signal_quality_score'] * 0.4 + 
                    confidence * 100 * 0.2)
            
            # Manage existing trades first
            self._manage_risk(day, price, score)
            
            # Open new trade if conditions are met
            if len(self.active_trades) < self.max_trades and score > 60:
                # Calculate position size based on quality
                size = self._calculate_position_size(score)
                
                # Don't trade if balance is too low
                if size < 100:
                    continue
                    
                # Create new trade
                trade = Trade(
                    instrument=self.instrument,
                    direction=signal['signal_type'],
                    price=price,
                    quality=score,
                    size=size
                )
                
                self.active_trades.append(trade)
                self.total_trades += 1
                
                print(f"{date_str}: OPEN {signal['signal_type']} at {price:.4f} "
                      f"(score {score:.1f}, size ${size:.2f})")
        
        # Close any remaining trades on the last day
        final_date = dates[-1].strftime('%Y-%m-%d') if dates else "Final day"
        for trade in list(self.active_trades):
            trade.close(closes[-1], "simulation_end")
            self.balance += trade.profit
            self.history.append(trade)
            
            if trade.profit > 0:
                self.win_count += 1
            else:
                self.loss_count += 1
                
            self.active_trades.remove(trade)
            print(f"{final_date}: CLOSE {trade.direction} at {closes[-1]:.4f}, profit {trade.profit:.2f}")

        # Print summary statistics
        win_rate = self.win_count / max(1, self.total_trades) * 100
        print(f"\n=== SIMULATION SUMMARY ===")
        print(f"Instrument: {self.instrument} ({self.timeframe})")
        print(f"Period: {len(closes)} days" + (f" ({dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')})" if dates else ""))
        print(f"Starting balance: $10,000.00")
        print(f"Final balance: ${self.balance:.2f}")
        print(f"Total profit/loss: ${self.balance - 10000:.2f}")
        print(f"Total trades: {self.total_trades}")
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Win/Loss: {self.win_count}/{self.loss_count}")

if __name__ == '__main__':
    sim = ComplexTradingSimulation(days=60)
    sim.run()
