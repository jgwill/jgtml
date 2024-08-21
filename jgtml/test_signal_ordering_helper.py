# tests/test_signal_ordering_helper.py

import pytest
import pandas as pd
from datetime import datetime
from jgtml.SignalOrderingHelper import create_fdb_entry_order

# Read the CSV file
df = pd.read_csv('tests/fdb_data/AUD-CAD_H1_cds_cache_24082107.csv')

# Extract signal_bar and current_bar
signal_bar = df.iloc[0].to_dict()
current_bar = df.iloc[1].to_dict()

def test_create_fdb_entry_order_invalid_due_to_valid_gator():
    result = create_fdb_entry_order(
        i="AUD/CAD",
        signal_bar=signal_bar,
        current_bar=current_bar,
        lots=1,
        tick_shift=2,
        quiet=True,
        valid_gator_mouth_open_in_mouth=True,
        validate_signal_out_of_mouth=True,
        t="H1",
        validation_timestamp=datetime.now(),
        verbose_level=0
    )
    
    assert result is None, "Expected the order to be invalid due to valid_gator"

if __name__ == "__main__":
    pytest.main()