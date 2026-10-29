"""Build data/recruits.csv from the raw recruiting-class spreadsheets in data/raw/.

Run:  python clean.py
"""
from pathlib import Path
import re

import pandas as pd

ROOT = Path(__file__).parent
RAW_DIR = ROOT / "data" / "raw"
OUTPUT = ROOT / "data" / "recruits.csv"

# One raw file per high-school graduation class.
CLASS_FILES = {2025: "2025s.csv", 2026: "2026s.csv", 2027: "2027s.csv"}

EVENTS = ["vt_high", "ub_high", "bb_high", "fx_high"]
SCORES = EVENTS + ["aa_high"]
RAW_SCORES = {"VT High": "vt_high", "UB High": "ub_high", "BB High": "bb_high",
              "FX High": "fx_high", "AA High": "aa_high"}

# The public dataset never includes birth dates or social media handles.
OUTPUT_COLUMNS = [
    "athlete", "grad_year", "level", "level_year", "club_gym", "state", "region",
    "country", "school", "committed", "vt_high", "ub_high", "bb_high", "fx_high",
    "aa_high", "is_elite", "has_perfect10", "rating",
]

GYM_RE = re.compile(r"^(.*?)\s*\((\w+)\)$")
LEVEL_RE = re.compile(r"^\s*([A-Za-z0-9&]+)\s*-\s*(\d{4})\s*$")
OTHER_SPORTS = {"CHEER", "TF", "T&F", "DIVING", "SOCCER", "POLEVAULT", "FLAG FOOTBALL"}
NOT_COMMITTED = {"", "uncommitted", "?"}


def split_gym(gym):
    """'WOGA (TX)' -> ('WOGA', 'TX'). Gyms without a state code keep their full name."""
    if not isinstance(gym, str) or not gym.strip():
        return None, None
    match = GYM_RE.match(gym.strip())
    if match:
        return match.group(1).strip(), match.group(2)
    return gym.strip(), None


def parse_region(value):
    """Return (region, country). 'R5' -> (5, 'USA'); 'I-Canada' -> (None, 'Canada')."""
    if not isinstance(value, str):
        return None, "USA"
    value = value.strip()
    if re.fullmatch(r"R[1-8]", value):
        return int(value[1]), "USA"
    if value.startswith("I-"):
        return None, value[2:].strip()
    return None, "USA"


def parse_level(value):
    """Return (level, level_year). '10-2024' -> ('Level 10', 2024); 'E-2023' -> ('Elite', 2023)."""
    if not isinstance(value, str) or not value.strip():
        return "Unknown", None
    match = LEVEL_RE.match(value)
    code, year = (match.group(1), int(match.group(2))) if match else (value.strip(), None)
    code = code.upper()
    if code in {"8", "9", "10"}:
        return f"Level {code}", year
    if code in {"E", "ELITE"}:
        return "Elite", year
    if code.startswith("X"):
        return "Xcel", year
    if code == "C" or code.startswith("C-"):
        return "College", year
    if code.startswith("RETIRED"):
        return "Retired", year
    if code in OTHER_SPORTS:
        return "Other sport", year
    return "Other", year


def clean_scores(scores: pd.DataFrame) -> pd.DataFrame:
    """Make scores numeric. 0 means the event wasn't competed. Rows with impossible
    scores (an event above 10 or an all-around above 40) are misaligned in the source
    spreadsheet, so all of that row's scores are cleared rather than trusted."""
    scores = scores.apply(pd.to_numeric, errors="coerce").mask(lambda s: s == 0)
    broken = (scores[EVENTS] > 10).any(axis=1) | (scores["aa_high"] > 40)
    scores.loc[broken, :] = float("nan")
    return scores


def rate(scores: pd.DataFrame) -> pd.Series:
    """Average of the four event highs, +1 for any perfect 10.
    Athletes missing an event are left unrated instead of being scored as 0."""
    events = scores[EVENTS]
    rating = events.mean(axis=1) + events.eq(10).any(axis=1).astype(int)
    return rating.where(events.notna().all(axis=1)).round(4)


def clean_class(raw: pd.DataFrame, grad_year: int) -> pd.DataFrame:
    raw = raw.dropna(subset=["Athlete"])
    out = pd.DataFrame({"athlete": raw["Athlete"].str.strip(), "grad_year": grad_year})

    out[["level", "level_year"]] = pd.DataFrame(
        [parse_level(v) for v in raw["Level"]], index=raw.index)
    out[["club_gym", "state"]] = pd.DataFrame(
        [split_gym(v) for v in raw["Gym"]], index=raw.index)
    out[["region", "country"]] = pd.DataFrame(
        [parse_region(v) for v in raw["Region"]], index=raw.index)

    school = raw["School"].fillna("").str.strip()
    out["school"] = school.replace("", None)
    out["committed"] = ~school.str.lower().isin(NOT_COMMITTED)

    scores = clean_scores(raw[list(RAW_SCORES)].rename(columns=RAW_SCORES))
    out[SCORES] = scores
    out["is_elite"] = out["level"].eq("Elite")
    out["has_perfect10"] = scores[EVENTS].eq(10).any(axis=1)
    out["rating"] = rate(scores)
    return out


def build(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    classes = [clean_class(pd.read_csv(raw_dir / name, dtype=str), year)
               for year, name in CLASS_FILES.items()]
    df = pd.concat(classes, ignore_index=True).drop_duplicates()
    df["region"] = df["region"].astype("Int64")
    df["level_year"] = df["level_year"].astype("Int64")
    return df[OUTPUT_COLUMNS]


if __name__ == "__main__":
    recruits = build()
    recruits.to_csv(OUTPUT, index=False)
    rated = recruits["rating"].notna().sum()
    print(f"Wrote {len(recruits):,} athletes ({rated:,} rated) to {OUTPUT.relative_to(ROOT)}")
