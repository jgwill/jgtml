"""The higher-timeframe join in `ptottf.create_ttf_csv`, on a synthetic fixture.

Two properties:

1. The default join is byte-identical to the output of commit 68737e3 (main before
   `htf_completed_only` existed). The golden file
   `fixtures/ttf_default_join_68737e3.txt` was written by that commit's
   `create_ttf_csv` on `build_workset()` below. The live HTF chart reads this
   output and legitimately shows the forming higher-timeframe bar.

2. With `htf_completed_only=True`, a base bar is joined to the last higher-timeframe
   bar that had CLOSED by the base bar's close, never to one closing later. A bar's
   close is the next bar's open; the last bar of a frame is still forming.

No data directory, network or settings file is touched: the CDS service, the
column-list writer and the output path are replaced by stubs.
"""
import os
import sys
import types

import numpy as np
import pandas as pd
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "jgtml"))

import ptottf  # noqa: E402

GOLDEN = os.path.join(HERE, "fixtures", "ttf_default_join_68737e3.txt")
HTF_COLUMNS = ["ao", "mfi_sq", "zcol"]
BASE_TF = "D1"
HIGHER_TFS = ["M1", "W1"]
W1_AO_OFFSET = 1000.0
M1_AO_OFFSET = 2000.0
ZERO_VOLUME_DAY = pd.Timestamp("2024-02-02")  # a Friday, dropped by dropna_volume


def build_workset():
    """Base D1 bars Mon-Fri, 2024-01-01 .. 2024-04-03, with W1 and M1 above them.

    W1 starts a week after the base (2024-01-08), so the first base week has no
    W1 bar at all. M1 starts a month before it. Each higher-timeframe bar k
    carries ao = offset + k, so a joined value names the bar it came from.
    """
    d1_index = pd.bdate_range("2024-01-01", "2024-04-03", name="Date")
    n = len(d1_index)
    steps = np.arange(n)
    d1 = pd.DataFrame(
        {
            "Open": 1.10 + steps * 0.001,
            "High": 1.11 + steps * 0.001,
            "Low": 1.09 + steps * 0.001,
            "Close": 1.105 + steps * 0.001,
            "Volume": 100 + steps,
            "ao": steps * 0.1,
            "mfi_sq": steps % 2,
            "zcol": np.where(steps % 2 == 0, "green", "red"),
        },
        index=d1_index,
    )
    d1.loc[ZERO_VOLUME_DAY, "Volume"] = 0

    w1_index = pd.date_range("2024-01-08", "2024-04-01", freq="W-MON", name="Date")
    k = np.arange(len(w1_index))
    w1 = pd.DataFrame(
        {
            "Volume": 1000 + k,
            "ao": W1_AO_OFFSET + k,
            "mfi_sq": k % 3,
            "zcol": [f"w{x}" for x in k],
        },
        index=w1_index,
    )

    m1_index = pd.date_range("2023-12-01", "2024-04-01", freq="MS", name="Date")
    k = np.arange(len(m1_index))
    m1 = pd.DataFrame(
        {
            "Volume": 5000 + k,
            "ao": M1_AO_OFFSET + k,
            "mfi_sq": k,
            "zcol": [f"m{x}" for x in k],
        },
        index=m1_index,
    )
    return {"M1": m1, "W1": w1, BASE_TF: d1}


def run_create_ttf(monkeypatch, out_dir, **kwargs):
    """Call create_ttf_csv on the synthetic workset. Returns (df, path written)."""
    workset = build_workset()
    monkeypatch.setattr(
        ptottf, "svc",
        types.SimpleNamespace(get_higher_cdf_datasets=lambda *a, **k: {
            tf: frame.copy() for tf, frame in workset.items()}))
    monkeypatch.setattr(
        ptottf, "jpov", types.SimpleNamespace(get_higher_tf_array=lambda t: list(HIGHER_TFS)))
    monkeypatch.setattr(ptottf, "write_patternname_columns_list", lambda *a, **k: None)
    written = []

    def fake_outfile(i, t, use_full=True, suffix="", ns="ttf", pn="ttf"):
        path = os.path.join(str(out_dir), f"{pn}{suffix}.csv")
        written.append(path)
        return path

    monkeypatch.setattr(ptottf, "get_ttf_outfile_fullpath", fake_outfile)
    df = ptottf.create_ttf_csv(
        "EUR/USD", BASE_TF, use_full=False, use_fresh=False, force_read=True,
        columns_list_from_higher_tf=list(HTF_COLUMNS), not_needed_columns=[],
        pn="synth", **kwargs)
    assert len(written) == 1, written
    return df, written[0]


def _read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


FORMING = pd.Timestamp.max  # close time of the last bar of a frame: it has not closed


def _close_times(opens):
    """Close of each bar = the next bar's open; the last bar is forming."""
    opens = pd.DatetimeIndex(opens).sort_values()
    closes = list(opens[1:]) + [FORMING]
    return pd.Series(closes, index=opens)


def _closed_by(htf_close, base_close):
    """Higher-timeframe bars that had closed by `base_close`. A forming bar never has."""
    return htf_close[(htf_close != FORMING) & (htf_close <= base_close)]


def test_default_join_is_byte_identical_to_68737e3(monkeypatch, tmp_path):
    _, path = run_create_ttf(monkeypatch, tmp_path)
    assert os.path.basename(path) == "synth.csv"
    assert _read_bytes(path) == _read_bytes(GOLDEN)


def test_explicit_false_is_the_default(monkeypatch, tmp_path):
    _, path = run_create_ttf(monkeypatch, tmp_path, htf_completed_only=False)
    assert os.path.basename(path) == "synth.csv"
    assert _read_bytes(path) == _read_bytes(GOLDEN)


def test_default_join_reads_the_forming_bar(monkeypatch, tmp_path):
    """Guard on the fixture: the default really does join bars that close later."""
    df, _ = run_create_ttf(monkeypatch, tmp_path)
    w1 = build_workset()["W1"]
    w1_close = _close_times(w1.index)
    base_close = _close_times(build_workset()[BASE_TF].index)
    later = [ts for ts, ao in df["ao_W1"].items()
             if w1_close[w1.index[int(float(ao) - W1_AO_OFFSET)]] > base_close[ts]]
    assert later, "fixture no longer exercises the forming-bar join"


@pytest.mark.parametrize("htf, offset", [("W1", W1_AO_OFFSET), ("M1", M1_AO_OFFSET)])
def test_completed_only_never_joins_a_bar_closing_after_the_base_bar(
        monkeypatch, tmp_path, htf, offset):
    df, path = run_create_ttf(monkeypatch, tmp_path, htf_completed_only=True)
    assert os.path.basename(path) == "synth" + ptottf.HTF_COMPLETED_ONLY_SUFFIX + ".csv"
    assert not df.empty

    workset = build_workset()
    htf_frame = workset[htf]
    htf_close = _close_times(htf_frame.index)
    # Base closes come from the frame BEFORE zero-volume bars are dropped:
    # Thursday 2024-02-01 closes when the (dropped) Friday bar opens.
    base_close = _close_times(workset[BASE_TF].index)

    for ts, row in df.iterrows():
        k = int(float(row[f"ao_{htf}"]) - offset)
        joined_open = htf_frame.index[k]
        eligible = _closed_by(htf_close, base_close[ts])
        assert joined_open in eligible.index, (ts, htf, joined_open)
        # It is the LAST such bar, not merely an earlier one.
        assert joined_open == eligible.index.max(), (ts, htf, joined_open)
        # The other joined columns come from the same bar.
        assert row[f"mfi_sq_{htf}"] == htf_frame.loc[joined_open, "mfi_sq"]
        assert row[f"zcol_{htf}"] == htf_frame.loc[joined_open, "zcol"]


def test_completed_only_boundaries(monkeypatch, tmp_path):
    df, _ = run_create_ttf(monkeypatch, tmp_path, htf_completed_only=True)
    w1 = build_workset()["W1"]
    week_of = lambda day: int(float(df.loc[pd.Timestamp(day), "ao_W1"]) - W1_AO_OFFSET)
    # Friday's close is the next Monday's open, which is the week's close:
    # the week is complete and Friday gets it. Thursday does not.
    assert w1.index[week_of("2024-01-19")] == pd.Timestamp("2024-01-15")
    assert w1.index[week_of("2024-01-18")] == pd.Timestamp("2024-01-08")
    # Friday 2024-02-02 has zero volume and is dropped. Thursday 2024-02-01 still
    # closes at that Friday's open, not at the next Monday's: no week completes.
    assert ZERO_VOLUME_DAY not in df.index
    assert w1.index[week_of("2024-02-01")] == pd.Timestamp("2024-01-22")
    # The last W1 bar (2024-04-01) is forming: the last base bar gets the one before.
    assert w1.index[week_of("2024-04-03")] == pd.Timestamp("2024-03-25")
    # Integer pattern columns stay integers, as in the default join.
    assert all(isinstance(x, (int, np.integer)) for x in df["mfi_sq_W1"])
    # Base bars with no completed W1 bar yet are dropped (dropna), not zero-filled:
    # the first one is Friday 2024-01-12, when the 2024-01-08 week completes.
    assert df.index.min() == pd.Timestamp("2024-01-12")


# --- The flag reaches create_ttf_csv from each entry point --------------------

class _NoTracer:
    def __init__(self, *a, **k):
        pass

    def trace_operation(self, *a, **k):
        import contextlib
        return contextlib.nullcontext("trace")

    def add_step(self, *a, **k):
        pass


@pytest.mark.parametrize("flag", [False, True])
@pytest.mark.parametrize("tracing", [False, True])
def test_ttfcli_passes_the_flag(monkeypatch, flag, tracing):
    import argparse
    import ttfcli
    args = argparse.Namespace(instrument="EUR/USD", timeframe="D1", full=False, fresh=False,
                              quotescount=-1, patternname="mz", columns_list_from_higher_tf=None,
                              htf_completed_only=flag)
    calls = []
    monkeypatch.setattr(ttfcli, "_parse_args", lambda: args)
    monkeypatch.setattr(ttfcli, "create_ttf_csv", lambda *a, **k: calls.append(k))
    monkeypatch.setattr(ttfcli, "_has_tracing", tracing)
    monkeypatch.setattr(ttfcli, "JGTTracer", _NoTracer, raising=False)
    ttfcli.main()
    assert [c["htf_completed_only"] for c in calls] == [flag]


def test_cli_flag_parses(monkeypatch):
    import argparse
    from mlclicommon import add_htf_completed_only_argument
    parser = add_htf_completed_only_argument(argparse.ArgumentParser())
    assert parser.parse_args([]).htf_completed_only is False
    assert parser.parse_args(["--htf_completed_only"]).htf_completed_only is True
    assert parser.parse_args(["-hco"]).htf_completed_only is True


@pytest.mark.parametrize("flag, name", [(False, "synth.csv"), (True, "synth_htfc.csv")])
def test_read_ttf_csv_reads_and_creates_the_mode_file(monkeypatch, tmp_path, flag, name):
    """mlfcli reaches create_ttf_csv through read_ttf_csv; each mode has its own file."""
    seen, looked_up = {}, []

    def fake_outfile(i, t, use_full=True, suffix="", ns="ttf", pn="ttf"):
        looked_up.append(f"{pn}{suffix}.csv")
        return os.path.join(str(tmp_path), looked_up[-1])

    monkeypatch.setattr(ptottf, "get_ttf_outfile_fullpath", fake_outfile)
    monkeypatch.setattr(ptottf, "create_ttf_csv", lambda *a, **k: seen.update(k) or "created")
    # The mode's file is absent, so read_ttf_csv creates it, in the same mode.
    assert ptottf.read_ttf_csv("EUR/USD", "D1", pn="synth", htf_completed_only=flag) == "created"
    assert looked_up == [name]
    assert seen["htf_completed_only"] is flag


@pytest.mark.parametrize("flag, name", [(False, "EUR-USD_D1_mz.csv"), (True, "EUR-USD_D1_mz_htfc.csv")])
def test_mlfcli_output_path_names_the_mode(monkeypatch, tmp_path, flag, name):
    import argparse
    import mlfcli
    monkeypatch.setenv("JGTPY_DATA", str(tmp_path))
    args = argparse.Namespace(instrument="EUR/USD", timeframe="D1", full=False,
                              patternname="mz", htf_completed_only=flag)
    assert os.path.basename(mlfcli._outfile_for(args)) == name


@pytest.mark.parametrize("flag", [False, True])
def test_mlfcli_wrapper_passes_the_flag(monkeypatch, flag):
    import argparse
    import mlfcli
    seen = {}
    monkeypatch.setattr(mlfcli.realityhelper, "generate_mlf_feature_pattern",
                        lambda *a, **k: seen.update(k))
    args = argparse.Namespace(instrument="EUR/USD", timeframe="D1", full=False, lag_period=1,
                              total_lagging_periods=5, columns_to_keep=None, columns_to_drop=None,
                              rmbidask=False, patternname="mz", htf_completed_only=flag)
    mlfcli.run_mlf_wrapper(args, False)
    assert seen["htf_completed_only"] is flag
    seen.clear()
    mlfcli.run_mlf_wrapper_with_tracing(args, False, None)
    assert seen["htf_completed_only"] is flag
    monkeypatch.undo()
    import inspect
    assert "htf_completed_only" in inspect.signature(
        mlfcli.realityhelper.generate_mlf_feature_pattern).parameters
