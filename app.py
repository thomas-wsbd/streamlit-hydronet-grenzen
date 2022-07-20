import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Grenzen HydroNET Provinciaal Meetnet - App",
    page_icon=":droplet:",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache
def load_df():
    df_result = pd.read_csv(
        "csv/dfresult.csv", index_col=[0], header=[0, 1], skipinitialspace=True
    )
    df_timeseries = pd.read_csv("csv/dftimeseries.csv", index_col=[0], parse_dates=[0])
    return df_result, df_timeseries


df_result, df_timeseries = load_df()

df_result_dt = pd.DataFrame(
    index=pd.date_range(start="2018-01-01", end="2022-07-01"), columns=df_result.columns
)
for year in df_result_dt.index.year.unique():
    dfr = df_result.copy()
    dfr.index = pd.to_datetime(year * 1000 + df_result.index, format="%Y%j")
    df_result_dt.fillna(dfr, inplace=True)
df_timeseries = df_timeseries["2018-01-01":"2022-07-01"]

locs = sorted(df_result.columns.get_level_values(0).unique().to_list())
if "index" not in st.session_state:
    st.session_state.index = 0

st.title("Grenzen HydroNET Provinciaal Meetnet - App")
controls = st.sidebar
loc = controls.selectbox("Meetpunt", options=locs, index=0)

button_next = controls.button("Volgende meetpunt")
button_back = controls.button("Vorige meetpunt")

if button_next:
    st.session_state.index += 1
    loc = locs[st.session_state.index]

if button_back:
    st.session_state.index -= 1
    loc = locs[st.session_state.index]

if loc:
    df_temp = df_result_dt[loc]
    df_temp.columns = ["droog", "matig droog", "normaal", "matig nat"]
    df_loc = df_temp.diff(axis="columns")
    df_loc["droog"] = df_temp["droog"]
    df_loc = df_loc.apply(pd.to_numeric, errors="coerce")  # convert columns to numeric
    df_loc["nat"] = 100.0

    fig = px.area(
        df_loc,
        title=loc,
        range_y=[int(df_timeseries[loc].min() - 1), int(df_timeseries[loc].max() + 2)],
        range_x=["2018-01-01", "2022-07-01"],
        labels={"value": "Stijghoogte (mNAP)"},
        color_discrete_sequence=[
            "red",
            "orange",
            "lightgreen",
            "lightblue",
            "blue",
            "navy",
        ],
        height=600,
    )

    fig.append_trace(
        px.scatter(df_timeseries[loc], color_discrete_sequence=["black"])["data"][0],
        1,
        1,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
