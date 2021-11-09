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
    df_timeseries_f1 = pd.read_csv(
        "csv/dftimeseriesf1.csv", index_col=[0], parse_dates=[0]
    )
    return df_result, df_timeseries_f1


df_result, df_timeseries_f1 = load_df()

locs = df_result.columns.get_level_values(0).unique().to_list()
if "index" not in st.session_state:
    st.session_state.index = 0
years = list(range(2000, 2022))

st.title("Grenzen HydroNET Provinciaal Meetnet - App")
controls = st.sidebar
loc = controls.selectbox("Meetpunt", options=locs, index=0)
year = controls.selectbox("Referentie jaar", options=years, index=21)

button_next = controls.button("Volgende meetpunt")
button_back = controls.button("Vorige meetpunt")

if button_next:
    st.session_state.index += 1
    loc = locs[st.session_state.index]

if button_back:
    st.session_state.index -= 1
    loc = locs[st.session_state.index]

if loc:
    fig = px.line(
        df_result[loc],
        title=loc,
        labels={"value": "Stijghoogte (mNAP", "DateTime": "Dagnummer"},
        height=600,
    )
    if year:
        df_ref = df_timeseries_f1.loc[str(year)]
        df_ref.index = df_ref.index.dayofyear
        fig.append_trace(
            px.scatter(df_ref[loc], color_discrete_sequence=["black"])["data"][0], 1, 1
        )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
