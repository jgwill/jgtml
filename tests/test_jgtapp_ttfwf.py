"""`jgtapp ttfwf` runs the patterns named by `ttf2run` in the JGT settings.

`jgtcommon.get_settings()` returns a dict. `ttfwf` used to test
`hasattr(settings, 'ttf2run')`, always False on a dict, so it ran only
TTF2RUN_DEFAULT (["mfi"]) whatever the settings said.
"""
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "jgtml"))

import jgtapp  # noqa: E402
from jgtutils import jgtcommon  # noqa: E402
from mlconstants import TTF2RUN_DEFAULT  # noqa: E402

CONFIGURED = ["mfi", "ttf", "zonesq", "mz"]


@pytest.fixture
def settings_home(monkeypatch, tmp_path):
    """A HOME and cwd holding only the settings the test writes; no settings cache."""
    for var in ["JGT_SETTINGS", "JGT_SETTINGS_USER", "JGT_SETTINGS_SYSTEM", "JGT_SETTINGS_PROCESS"]:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(jgtcommon, "settings", None)
    load_from_path = jgtcommon._load_settings_from_path
    monkeypatch.setattr(jgtcommon, "_load_settings_from_path",  # ignore this host's /etc/jgt
                        lambda path: {} if path.startswith("/etc") else load_from_path(path))
    (tmp_path / ".jgt").mkdir()

    def write(settings):
        (tmp_path / ".jgt" / "settings.json").write_text(json.dumps(settings))
    return write


def _run_ttfwf(monkeypatch):
    calls = []
    monkeypatch.setattr(jgtapp, "cds", lambda *a, **k: None)
    monkeypatch.setattr(jgtapp, "ttf", lambda instrument, t, pn="ttf", **k: calls.append((pn, t)))
    jgtapp.ttfwf("EUR/USD")
    return calls


def test_settings_are_a_dict(settings_home):
    settings_home({"ttf2run": CONFIGURED})
    settings = jgtcommon.get_settings()
    assert isinstance(settings, dict)
    assert not hasattr(settings, "ttf2run")  # why the old check never matched


def test_ttfwf_runs_the_configured_patterns(monkeypatch, settings_home):
    settings_home({"ttf2run": CONFIGURED})
    calls = _run_ttfwf(monkeypatch)
    assert [pn for pn, _ in calls] == [pn for pn in CONFIGURED for _ in ("W1", "D1", "H4")]
    assert [t for _, t in calls] == ["W1", "D1", "H4"] * len(CONFIGURED)


@pytest.mark.parametrize("settings", [{}, {"ttf2run": []}, {"ttf2run": None}])
def test_ttfwf_falls_back_to_the_default(monkeypatch, settings_home, settings):
    settings_home(settings)
    calls = _run_ttfwf(monkeypatch)
    assert sorted({pn for pn, _ in calls}) == sorted(TTF2RUN_DEFAULT)
