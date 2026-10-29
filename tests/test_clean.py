import io
import math

import pandas as pd
import pytest

import clean


@pytest.mark.parametrize("gym, expected", [
    ("WOGA (TX)", ("WOGA", "TX")),
    ("Silvia's  (PA)", ("Silvia's", "PA")),
    ("Bull City (NC)/ Alabama", ("Bull City (NC)/ Alabama", None)),
    (None, (None, None)),
])
def test_split_gym(gym, expected):
    assert clean.split_gym(gym) == expected


@pytest.mark.parametrize("value, expected", [
    ("R5", (5, "USA")),
    ("I-Canada", (None, "Canada")),
    ("C-FR", (None, "USA")),
    (None, (None, "USA")),
])
def test_parse_region(value, expected):
    assert clean.parse_region(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("10-2024", ("Level 10", 2024)),
    ("9-2025", ("Level 9", 2025)),
    ("e-2023", ("Elite", 2023)),
    ("XSA-2025", ("Xcel", 2025)),
    ("C-fr", ("College", None)),
    ("Retired 2025", ("Retired", None)),
    ("t&f", ("Other sport", None)),
    (None, ("Unknown", None)),
])
def test_parse_level(value, expected):
    assert clean.parse_level(value) == expected


def scores(*rows):
    return pd.DataFrame(rows, columns=clean.SCORES)


def test_zero_means_event_not_competed():
    out = clean.clean_scores(scores(["9.5", "0", "9.4", "9.6", "28.5"]))
    assert math.isnan(out.loc[0, "ub_high"])


def test_misaligned_row_is_cleared():
    # The all-around score landed in the floor column in the source spreadsheet.
    out = clean.clean_scores(scores(["9.2", "8.925", "9.475", "36.15", "fhs pike"]))
    assert out.loc[0].isna().all()


def test_rating_averages_events_with_perfect_10_bonus():
    s = clean.clean_scores(scores(["9.5", "9.5", "9.5", "9.5", "38"], ["10", "9.6", "9.4", "9.8", "38.8"]))
    rating = clean.rate(s)
    assert rating[0] == pytest.approx(9.5)
    assert rating[1] == pytest.approx(9.7 + 1)


def test_rating_left_blank_when_an_event_is_missing():
    s = clean.clean_scores(scores(["9.5", "", "9.5", "9.5", "28.5"]))
    assert math.isnan(clean.rate(s)[0])


def test_committed_flag():
    raw = pd.DataFrame({
        "Athlete": ["A", "B", "C"], "Gym": ["X (CA)"] * 3, "Region": ["R7"] * 3,
        "School": ["UCLA", "Uncommitted", None], "Level": ["10-2025"] * 3,
        **{col: ["9.5"] * 3 for col in clean.RAW_SCORES},
    })
    out = clean.clean_class(raw, 2026)
    assert out["committed"].tolist() == [True, False, False]


def test_built_dataset_has_no_personal_information():
    df = clean.build()
    assert list(df.columns) == clean.OUTPUT_COLUMNS
    for banned in ("dob", "insta"):
        assert not any(banned in c.lower() for c in df.columns)
    assert not df.astype(str).apply(lambda col: col.str.contains("instagram.com")).any().any()


def test_committed_dataset_is_up_to_date():
    """data/recruits.csv must match what clean.py builds. If this fails, run `python clean.py`."""
    committed = pd.read_csv(clean.OUTPUT)
    rebuilt = pd.read_csv(io.StringIO(clean.build().to_csv(index=False)))
    pd.testing.assert_frame_equal(committed, rebuilt)
