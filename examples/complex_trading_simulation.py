import random
from datetime import datetime
from typing import List

from jgtml.fdb_signal_quality_predictor import FDBSignalQualityPredictor

class Trade:
    def __init__(self, instrument: str, direction: str, price: float, quality: float):
        self.instrument = instrument
        self.direction = direction
        self.entry_price = price
        self.quality = quality
        self.open_time = datetime.now()
        self.close_time = None
        self.exit_price = None
        self.profit = 0.0

    def close(self, price: float):
        self.exit_price = price
        self.close_time = datetime.now()
        if self.direction == 'buy':
            self.profit = price - self.entry_price
        else:
            self.profit = self.entry_price - price

class ComplexTradingSimulation:
    """Simulate a series of trades using FDBSignalQualityPredictor."""

    def __init__(self, instrument: str = 'EUR-USD', timeframe: str = 'D1', days: int = 30):
        self.instrument = instrument
        self.timeframe = timeframe
        self.days = days
        self.predictor = FDBSignalQualityPredictor(data_path='samples')
        self.history: List[Trade] = []
        self.balance = 10_000.0

    def _generate_market_data(self) -> List[float]:
        prices = [1.0]
        for _ in range(self.days):
            prices.append(prices[-1] + random.uniform(-0.01, 0.01))
        return prices

    def _generate_signal(self):
        return {
            'signal_type': random.choice(['buy', 'sell']),
            'strength': random.random(),
            'context': random.choice(['fractal_breakout', 'trend_reversal', 'momentum_spike'])
        }

    def run(self):
        prices = self._generate_market_data()
        active_trade = None
        for day in range(1, len(prices)):
            price = prices[day]
            signal = self._generate_signal()
            quality = self.predictor.evaluate_signal(self.instrument, self.timeframe, signal)
            score = quality['overall_quality_score']

            if not active_trade and score > 60:
                active_trade = Trade(self.instrument, signal['signal_type'], price, score)
                print(f"Day {day}: OPEN {signal['signal_type']} at {price:.4f} (score {score:.1f})")
            elif active_trade:
                if (active_trade.direction == 'buy' and price - active_trade.entry_price > 0.005) or \
                   (active_trade.direction == 'sell' and active_trade.entry_price - price > 0.005) or \
                   score < 40:
                    active_trade.close(price)
                    self.balance += active_trade.profit
                    self.history.append(active_trade)
                    print(f"Day {day}: CLOSE at {price:.4f}, profit {active_trade.profit:.4f}")
                    active_trade = None
        if active_trade:
            active_trade.close(prices[-1])
            self.balance += active_trade.profit
            self.history.append(active_trade)
            print(f"Final day: CLOSE at {prices[-1]:.4f}, profit {active_trade.profit:.4f}")

        print(f"Final balance: {self.balance:.2f}")

if __name__ == '__main__':
    sim = ComplexTradingSimulation()
    sim.run()
