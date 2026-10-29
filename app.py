"""Streamlit dashboard for the NCAA women's gymnastics recruit database."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parent / "data" / "recruits.csv"
GYM_LEVELS = ["Elite", "Level 10", "Level 9", "Level 8"]
METRICS = {"Rating": "rating", "All-around": "aa_high", "Vault": "vt_high",
           "Bars": "ub_high", "Beam": "bb_high", "Floor": "fx_high"}

st.set_page_config(page_title="NCAA Gymnastics Recruits", page_icon="🤸", layout="wide")


@st.cache_data
def load() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    df["region_label"] = df["region"].map(lambda r: f"Region {int(r)}" if pd.notna(r) else None)
    df.loc[df["country"] != "USA", "region_label"] = "International"
    return df


df = load()

st.title("🤸 NCAA Gymnastics Recruit Database")
st.caption(
    f"{len(df):,} gymnasts from the high school classes of 2025–2027, compiled from public "
    "commitment announcements. Scores are each athlete's season highs."
)

# ---- Filters ----------------------------------------------------------------
with st.sidebar:
    st.header("Filters")
    classes = st.multiselect("Class", sorted(df["grad_year"].unique()), default=sorted(df["grad_year"].unique()))
    levels = st.multiselect("Level", GYM_LEVELS + sorted(set(df["level"]) - set(GYM_LEVELS)), default=GYM_LEVELS)
    regions = st.multiselect("Region", sorted(df["region_label"].dropna().unique(), key=lambda r: (r == "International", r)))
    committed_only = st.toggle("Committed athletes only")
    schools = st.multiselect("Committed to", sorted(df.loc[df["committed"], "school"].unique()))
    name = st.text_input("Search by name")

view = df[df["grad_year"].isin(classes) & df["level"].isin(levels)]
if regions:
    view = view[view["region_label"].isin(regions)]
if committed_only:
    view = view[view["committed"]]
if schools:
    view = view[view["school"].isin(schools)]
if name:
    view = view[view["athlete"].str.contains(name, case=False, na=False)]

# ---- Summary ----------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Athletes", f"{len(view):,}")
c2.metric("Committed", f"{int(view['committed'].sum()):,}")
c3.metric("Rated (all 4 events)", f"{int(view['rating'].notna().sum()):,}")
avg = view["rating"].mean()
c4.metric("Average rating", f"{avg:.3f}" if pd.notna(avg) else "–")

with st.expander("How the rating works"):
    st.markdown(
        "**Rating = average of the four event highs (vault, bars, beam, floor), "
        "+1 if the athlete has scored a perfect 10.0 on any event.**\n\n"
        "- Event highs make athletes comparable even when they never competed all four events at the same meet.\n"
        "- Athletes missing an event are left unrated instead of being scored as 0, which would rank them unfairly low.\n"
        "- Scores of 0 in the source data mean the event wasn't competed, so they're treated as missing."
    )

leaderboard, schools_tab, regions_tab, data_tab = st.tabs(["Leaderboard", "Schools", "Regions", "All data"])

# ---- Leaderboard --------------------------------------------------------------
with leaderboard:
    left, right = st.columns([1, 2])
    metric_label = left.selectbox("Rank by", list(METRICS))
    top_n = right.slider("Show top", 10, 100, 25, step=5)
    metric = METRICS[metric_label]
    top = (view.dropna(subset=[metric]).sort_values(metric, ascending=False).head(top_n)
           .reset_index(drop=True))
    top.index += 1
    st.dataframe(
        top[["athlete", "grad_year", "level", "club_gym", "state", "school", "rating",
             "aa_high", "vt_high", "ub_high", "bb_high", "fx_high"]],
        column_config={
            "athlete": "Athlete", "grad_year": st.column_config.NumberColumn("Class", format="%d"),
            "level": "Level", "club_gym": "Club", "state": "State", "school": "School",
            "rating": st.column_config.NumberColumn("Rating", format="%.3f"),
            "aa_high": st.column_config.NumberColumn("AA", format="%.3f"),
            "vt_high": st.column_config.NumberColumn("VT", format="%.3f"),
            "ub_high": st.column_config.NumberColumn("UB", format="%.3f"),
            "bb_high": st.column_config.NumberColumn("BB", format="%.3f"),
            "fx_high": st.column_config.NumberColumn("FX", format="%.3f"),
        },
        width="stretch",
    )

# ---- Schools ------------------------------------------------------------------
with schools_tab:
    commits = view[view["committed"]]
    if commits.empty:
        st.info("No committed athletes match these filters.")
    else:
        by_school = (commits.groupby("school")
                     .agg(commits=("athlete", "count"), avg_rating=("rating", "mean"))
                     .sort_values(["commits", "avg_rating"], ascending=False).head(20).reset_index())
        by_school["label"] = by_school["avg_rating"].map(
            lambda r: f"avg rating {r:.2f}" if pd.notna(r) else "unrated")
        fig = px.bar(by_school, x="commits", y="school", orientation="h", text="label",
                     labels={"commits": "Commits", "school": ""},
                     title="Schools with the most commits (top 20)")
        fig.update_traces(marker_color="#552583", textposition="outside", cliponaxis=False)
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=620,
                          margin={"r": 120})
        st.plotly_chart(fig, width="stretch")

# ---- Regions ------------------------------------------------------------------
with regions_tab:
    rated = view.dropna(subset=["rating", "region_label"])
    if rated.empty:
        st.info("No rated athletes match these filters.")
    else:
        order = sorted(rated["region_label"].unique(), key=lambda r: (r == "International", r))
        fig = px.box(rated, x="region_label", y="rating", points="outliers",
                     category_orders={"region_label": order},
                     labels={"region_label": "USA Gymnastics region", "rating": "Rating"},
                     title="Rating distribution by region")
        st.plotly_chart(fig, width="stretch")
        counts = view["region_label"].value_counts().reindex(order).rename("Athletes")
        st.bar_chart(counts)

# ---- All data -----------------------------------------------------------------
with data_tab:
    st.dataframe(view.drop(columns=["region_label"]), width="stretch", hide_index=True)
    st.download_button("Download these results (CSV)", view.drop(columns=["region_label"]).to_csv(index=False),
                       file_name="gymnastics_recruits.csv", mime="text/csv")
