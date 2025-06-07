import random
from datetime import datetime
from typing import List

from jgtml.fdb_signal_quality_predictor import FDBSignalQualityPredictor
from jgtml.fdb_pattern_intelligence import FDBPatternIntelligence
from jgtml.fdb_scanner_2408 import generate_fresh_and_cache

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
        self.balance = 10_000.0

    def _generate_market_data(self) -> List[float]:
        prices = [1.0]
        for _ in range(self.days):
            prices.append(prices[-1] + random.uniform(-0.01, 0.01))
        return prices

    def _random_signal(self):
        """Generate a random fallback signal."""
        return {
            'signal_type': random.choice(['buy', 'sell']),
            'strength': random.random(),
            'context': random.choice(['fractal_breakout', 'trend_reversal', 'momentum_spike'])
        }

    def _scan_signal(self):
        """Scan the latest market data using FDBScanner."""
        try:
            df = generate_fresh_and_cache(self.instrument.replace('-', '/'), self.timeframe)
            last = df.iloc[-1]
            if last.get('fdbb', 0) == 1:
                sig_type = 'sell'
            elif last.get('fdbs', 0) == 1:
                sig_type = 'buy'
            else:
                return self._random_signal()

            return {
                'signal_type': sig_type,
                'strength': abs(last.get('ao', 0)),
                'context': 'scanner_realtime'
            }
        except Exception as e:
            print(f"⚠️ Scanner failed: {e} -- using random signal.")
            return self._random_signal()

    def run(self):
        prices = self._generate_market_data()
        active_trade = None
        for day in range(1, len(prices)):
            price = prices[day]
            signal = self._scan_signal()
            quality = self.predictor.evaluate_signal(self.instrument, self.timeframe, signal)
            intel = self.intelligence.evaluate_fdb_signal(self.instrument, self.timeframe, 'bull' if signal['signal_type'] == 'buy' else 'bear')
            score = (quality['overall_quality_score'] + intel['signal_quality_score']) / 2

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
