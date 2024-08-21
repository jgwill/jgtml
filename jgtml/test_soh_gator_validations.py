import unittest
from unittest.mock import patch
from jgtml.SignalOrderingHelper import valid_gator

class TestValidGator(unittest.TestCase):

  def test_valid_gator_returns_true(self):
    last_bar_completed = {
      'HIGH': 0.91735,
      'LOW': 0.91642,
      'FDB': 0,
      'ASKHIGH': 0.91789748219,
      'BIDLOW': 0.91014196311,
      'JAW': 0.90529160356,
      'TEETH': 0.90529160356,
      'LIPS': 0.90529160356
    }
    current_bar = {
      'HIGH': 0.91698,
      'LOW': 0.91667,
      'FDB': 0,
      'ASKHIGH': 0.9179434451,
      'BIDLOW': 0.9101070839,
      'JAW': 0.90530824173,
      'TEETH': 0.90530824173,
      'LIPS': 0.90530824173
    }
    bs = "B"

    result = valid_gator(last_bar_completed, current_bar, bs)

    self.assertTrue(result)

  def test_valid_gator_returns_false(self):
    last_bar_completed = {
      'HIGH': 0.91735,
      'LOW': 0.91642,
      'FDB': 0,
      'ASKHIGH': 0.91789748219,
      'BIDLOW': 0.91014196311,
      'JAW': 0.90529160356,
      'TEETH': 0.90529160356,
      'LIPS': 0.90529160356
    }
    current_bar = {
      'HIGH': 0.91698,
      'LOW': 0.91667,
      'FDB': 0,
      'ASKHIGH': 0.9179434451,
      'BIDLOW': 0.9101070839,
      'JAW': 0.90530824173,
      'TEETH': 0.90530824173,
      'LIPS': 0.90530824173
    }
    bs = "S"

    result = valid_gator(last_bar_completed, current_bar, bs)

    self.assertFalse(result)

if __name__ == "__main__":
  unittest.main()