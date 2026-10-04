"""
Q/A:

1. Where did you use caching, and why?
    On load_data() using @st.cache_data, so the csv isn't reloaded every time someone clicks a filter.

2. Which variable did you store using Session State?
    st.session_state.notes, to keep feedback notes saved across reruns and page changes.

3. Which widget had the biggest effect on the displayed data?
    The track selectbox and status multiselect, because they filter out most of the rows and update all the kpis and charts.

4. What happens in your app when filters return no rows?
    It shows a warning message saying no records matched instead of crashing.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Training Center Dashboard", layout="wide")

# load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv("workshops.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

raw_df = load_data()

# save notes in session state
if "notes" not in st.session_state:
    st.session_state.notes = []

# sidebar navigation and filters
st.sidebar.title("Navigation & Filters")
page = st.sidebar.radio("Go to:", ["Overview", "Dataset Explorer", "Insights", "Feedback"])

track = st.sidebar.selectbox("Track:", ["All"] + sorted(raw_df["track"].dropna().unique().tolist()))
status = st.sidebar.multiselect("Status:", raw_df["status"].dropna().unique().tolist(), default=raw_df["status"].dropna().unique().tolist())
min_rating = st.sidebar.slider("Min Rating:", 1.0, 5.0, 4.0, 0.1)
dates = st.sidebar.date_input("Date Range:", (raw_df["date"].min().date(), raw_df["date"].max().date()))
min_learners = st.sidebar.number_input("Min Learners:", 0, 100, 0, 5)
show_raw = st.sidebar.checkbox("Show Raw Dataset", False)

# apply filters
df = raw_df.copy()
if track != "All":
    df = df[df["track"] == track]
if status:
    df = df[df["status"].isin(status)]
else:
    df = df.iloc[0:0]
df = df[(df["rating"] >= min_rating) | (df["rating"].isna())]
df = df[(df["learners"] >= min_learners) | (df["learners"].isna())]
if isinstance(dates, (tuple, list)) and len(dates) == 2:
    df = df[(df["date"].dt.date >= dates[0]) & (df["date"].dt.date <= dates[1])]

# overview page
if page == "Overview":
    st.image("banner.png", caption="Training Center Workshop Dashboard")
    st.title("Workshop Performance Overview")
    st.caption("Samsung Innovation Campus - Streamlit Task")
    st.markdown("Inspect workshop delivery, participant attendance, ratings, and costs.")

    st.header("Executive KPIs")
    if df.empty:
        st.warning("No records match the selected filters.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Learners", f"{int(df['learners'].sum()):,}", delta=f"{int(df['learners'].sum() - raw_df['learners'].sum()):,} vs All")
        c2.metric("Average Rating", f"{df['rating'].mean():.2f}", delta=f"{df['rating'].mean() - raw_df['rating'].mean():+.2f} vs All")
        c3.metric("Total Cost", f"${df['cost'].sum():,.0f}", delta=f"${df['cost'].sum() - raw_df['cost'].sum():+,.0f} vs All")

    st.subheader("Metric Formula")
    st.write("Average rating is calculated dynamically across filtered records:")
    st.latex(r"\text{Average Rating} = \frac{1}{N} \sum_{i=1}^{N} \text{Rating}_i")
    st.code("avg_rating = df['rating'].mean()", language="python")

    st.subheader("Dataset Summary")
    st.write(f"- Total rows: {len(raw_df)} | Missing values: {raw_df.isna().sum().sum()} | Duplicates: {raw_df.duplicated('course').sum()}")

# explorer page
elif page == "Dataset Explorer":
    st.title("Dataset Explorer")
    st.caption("Filter, view, and edit workshop records.")

    search = st.text_input("Search Course Name:", "")
    view_df = df[df["course"].str.contains(search, case=False, na=False)] if search else df

    st.header("Filtered Workshops")
    if view_df.empty:
        st.warning("No records match your filters.")
    else:
        st.dataframe(view_df)

    st.subheader("Summary Table by Track")
    if not df.empty:
        st.table(df.groupby("track")[["learners", "rating", "cost"]].mean().round(2))

    st.subheader("Edit Records")
    st.caption("Edit rating, status, or cost directly:")
    st.data_editor(view_df[["course", "rating", "cost", "status"]], key="editor")

# insights page
elif page == "Insights":
    st.title("Insights & Analysis")
    st.caption("Visualizing attendance and category performance.")

    if df.empty:
        st.warning("No records match the selected filters.")
    else:
        st.header("Key Analytical Findings")
        top_track = raw_df.groupby("track")["rating"].mean().idxmax()
        top_city = raw_df.groupby("city")["learners"].sum().idxmax()
        flagged = raw_df[(raw_df["rating"] < 4.5) | (raw_df["cost"] > 2500)]["course"].tolist()

        st.write(f"1. **Highest rated track:** {top_track} ({raw_df.groupby('track')['rating'].mean().max():.2f} ⭐)")
        st.write(f"2. **City with most learners:** {top_city} ({int(raw_df.groupby('city')['learners'].sum().max()):,} learners)")
        st.write(f"3. **Courses with low rating (<4.5) or high cost (>$2500):** {', '.join(flagged[:4])}...")

        st.subheader("Learners by Category (Bar Chart)")
        group_col = st.radio("Group By:", ["track", "city", "status"], horizontal=True)
        st.bar_chart(df.groupby(group_col)["learners"].sum())

        st.subheader("Attendance Trend Over Time (Line Chart)")
        st.line_chart(df.dropna(subset=["date"]).groupby(df["date"].dt.date)["learners"].sum())

# feedback page
elif page == "Feedback":
    st.title("Feedback & Session State")
    st.caption("Demonstrating persistence across reruns using st.session_state.")

    st.header("Add Note")
    note = st.text_input("Enter your feedback note:")
    if st.button("Save Note") and note.strip():
        st.session_state.notes.append(note.strip())
        st.success("Note saved to session state!")

    st.subheader("Saved Notes History")
    if st.session_state.notes:
        for i, n in enumerate(reversed(st.session_state.notes), 1):
            st.write(f"{i}. {n}")
    else:
        st.write("No notes recorded yet in this session.")

# optional raw data
if show_raw:
    st.divider()
    st.subheader("Raw Dataset")
    st.dataframe(raw_df)
