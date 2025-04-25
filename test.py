import streamlit as st
import pandas as pd
import altair as alt
import os

# Streamlit page configuration
st.set_page_config(
    page_title="FCK Superliga Tabel",
    page_icon="https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8391/teamlogo.png",
    layout="wide"
)

# Custom font and CSS
st.markdown("""
    <style>
    @font-face {
        font-family: 'FCKSerifBold';
        src: url('https://raw.githubusercontent.com/nrssp/Test/d62a85fd81fa5d438140f0d5af7e1b4bf44d2489/FCKSerif-Bold.ttf') format('truetype');
    }

    @font-face {
        font-family: 'FCKTextSemiBold';
        src: url('https://raw.githubusercontent.com/nrssp/Test/fc9ee1c1f14f9038c3b0c4c3b8dee274a7f74adf/FCKText-SemiBold.ttf') format('truetype');
    }

    html, body, [class*="css"] {
        font-family: 'FCKTextSemiBold', sans-serif;
    }

    section[data-testid="stSidebar"] * {
        font-family: 'FCKSerifBold', serif !important;
    }

    /* Kun overskrifter i sidebaren skal have underline */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        font-size: 1.1rem !important;
        font-weight: bold !important;
        font-family: 'FCKSerifBold', serif !important;
        text-decoration: underline !important;
    }

    /* Filtrenes labels skal være fede men uden underline */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stTextInput label,
    section[data-testid="stSidebar"] .stNumberInput label,
    section[data-testid="stSidebar"] .stCheckbox label {
        font-size: 1.1rem !important;
        font-family: 'FCKSerifBold', serif !important;
        text-decoration: none !important;
        font-weight: bold !important;
    }

    section[data-testid="stSidebar"] .stSlider div[data-testid="stSliderLabel"] {
        font-size: 1.1rem !important;
        font-family: 'FCKSerifBold', serif !important;
        text-decoration: none !important;
        font-weight: bold !important;
    }

    h1 {
        font-family: 'FCKSerifBold', serif !important;
        font-size: 3.5rem !important;
        text-decoration: none;
    }

    .centered-header th {
        text-align: center !important;
        background-color: #011a8b !important;
        color: white !important;
    }
    .kampoversigt th {
        text-align: center !important;
        background-color: #011a8b !important;
        color: white !important;
    }
    .kampoversigt td {
        text-align: center !important;
    }
    table tr:hover td {
        background-color: #f1f1f1;
    }
    </style>
""", unsafe_allow_html=True)

# Load CSV with match results
csv_url = "https://raw.githubusercontent.com/nrssp/Test/main/superliga_kampresultater.csv"

try:
    df = pd.read_csv(csv_url)
except FileNotFoundError:
    st.error(f"Could not find CSV file at {csv_url}. Please ensure the file exists.")
    st.stop()

# Validate required columns
required_columns = ["Home", "Away", "Home Goals", "Away Goals", "Season", "Round", "Date"]
if not all(col in df.columns for col in required_columns):
    st.error("CSV file is missing required columns: " + ", ".join([col for col in required_columns if col not in df.columns]))
    st.stop()

# Header with FCK branding
st.markdown("""
    <div style='display: flex; align-items: center; gap: 20px;'>
        <img src='https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8391/teamlogo.png' width='60'>
        <h1 style='margin: 0; color: #011a8b;'>F.C. København – Superliga Tabel</h1>
    </div>
    <hr style='margin-top: 10px; margin-bottom: 30px; border: 1px solid #011a8b;'>
""", unsafe_allow_html=True)




# Custom CSS for FCK style
table_style = """
    <style>
    .centered-header th {
        text-align: center !important;
        background-color: #011a8b !important;
        color: white !important;
    }
    .kampoversigt th {
        text-align: center !important;
        background-color: #011a8b !important;
        color: white !important;
    }
    .kampoversigt td {
        text-align: center !important;
    }
    table tr:hover td {
        background-color: #f1f1f1;
    }
    </style>
"""
st.markdown(table_style, unsafe_allow_html=True)

# Sidebar: Season selection
# Reset filters button
if st.sidebar.button("Nulstil alle filtre", key="reset_filters"):
    keys_to_keep = []
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    st.session_state["selected_optional"] = ["MP", "W", "D", "L", "GF", "GA", "GD", "Pts/MP", "Form"]
    st.rerun()

all_seasons = sorted(df["Season"].unique(), reverse=True)
if "selected_specific_seasons" not in st.session_state:
    st.session_state["selected_specific_seasons"] = [all_seasons[0]]
if "select_all_toggle" not in st.session_state:
    st.session_state["select_all_toggle"] = True
if "Vis Championship-hold" not in st.session_state:
    st.session_state["Vis Championship-hold"] = True
if "Vis Relegation-hold" not in st.session_state:
    st.session_state["Vis Relegation-hold"] = True
if "Hjemmekampe" not in st.session_state:
    st.session_state["Hjemmekampe"] = True
if "Udekampe" not in st.session_state:
    st.session_state["Udekampe"] = True

# Her fortsætter den fulde oprindelige kode

selected_specific_seasons = st.sidebar.multiselect(
    "Vælg sæson",
    options=all_seasons,
    default=st.session_state.get("selected_specific_seasons", [all_seasons[0]]),
    key="selected_specific_seasons"
)

if selected_specific_seasons:
    selected_seasons = selected_specific_seasons
else:
    selected_seasons = all_seasons

df = df[df["Season"].isin(selected_seasons)]

# Sidebar: Round selection
min_round = int(df["Round"].astype(int).min())
max_round = int(df["Round"].astype(int).max())
selected_round_range = st.sidebar.slider(
    "Vælg rundeinterval",
    min_value=min_round,
    max_value=max_round,
    value=st.session_state.get("selected_round_range", (min_round, max_round)),
    key="selected_round_range"
)

all_rounds = sorted(df["Round"].astype(int).unique())
selected_specific_rounds = st.sidebar.multiselect(
    "Vælg runde/r",
    options=all_rounds,
    default=st.session_state.get("selected_specific_rounds", []),
    key="selected_specific_rounds"
)

# Sidebar: Championship/Relegation teams toggle
championship_teams = df[df["League"] == "championship round"]["Home"].unique().tolist()
relegation_teams = df[df["League"] == "relegation round"]["Home"].unique().tolist()

st.sidebar.header("Vis/Skjul grupper")
show_championship = st.sidebar.checkbox(
    "Hold i mesterskabsspillet",
    value=st.session_state.get("Vis Championship-hold", True),
    key="Vis Championship-hold"
)
show_relegation = st.sidebar.checkbox(
    "Hold i nedrykningsslutspillet",
    value=st.session_state.get("Vis Relegation-hold", True),
    key="Vis Relegation-hold"
)

# Sidebar: Team selection
visningsnavn_map = {
    "Midtjylland": "FC Midtjylland",
    "FC Copenhagen": "FC København",
    "Brøndby": "Brøndby IF",
    "Randers": "Randers FC",
    "Silkeborg": "Silkeborg IF",
    "Nordsjælland": "FC Nordsjælland",
    "Viborg": "Viborg FF",
    "Aalborg": "AAB",
    "Lyngby": "Lyngby BK"
}

teams = sorted(pd.unique(df[["Home", "Away"]].values.ravel()))
filtered_teams = [
    team for team in teams if
    (team in championship_teams and show_championship) or
    (team in relegation_teams and show_relegation) or
    (team not in championship_teams and team not in relegation_teams)
]
filtered_teams = sorted(filtered_teams, key=lambda team: visningsnavn_map.get(team, team))

st.sidebar.header("Vis/Skjul hold i tabel")
select_all_changed = st.sidebar.checkbox(
    "Vælg/fravælg alle",
    value=st.session_state.get("select_all_toggle", True),
    key="select_all_toggle"
)
previous_toggle = st.session_state.get("_previous_select_all", None)
st.session_state["_previous_select_all"] = select_all_changed
if previous_toggle is not None and previous_toggle != select_all_changed:
    for team in filtered_teams:
        st.session_state[f"toggle_{team}"] = select_all_changed

selected_teams = []
for team in filtered_teams:
    toggle_key = f"toggle_{team}"
    visningsnavn = visningsnavn_map.get(team, team)
    if toggle_key not in st.session_state:
        st.session_state[toggle_key] = select_all_changed
    if st.sidebar.checkbox(visningsnavn, value=st.session_state[toggle_key], key=toggle_key):
        selected_teams.append(team)

st.sidebar.header("Hjemme/Ude")
show_home = st.sidebar.checkbox(
    "Hjemmekampe",
    value=st.session_state.get("Hjemmekampe", True),
    key="Hjemmekampe"
)
show_away = st.sidebar.checkbox(
    "Udekampe",
    value=st.session_state.get("Udekampe", True),
    key="Udekampe"
)

# Create home/away dataframes
home_df = df[["Home", "Away", "Home Goals", "Away Goals", "Date"]].copy()
home_df.columns = ["Team", "Opponent", "Goals For", "Goals Against", "Date"]
home_df["Result"] = home_df.apply(
    lambda row: "W" if row["Goals For"] > row["Goals Against"] else "L" if row["Goals For"] < row["Goals Against"] else "D",
    axis=1
)

away_df = df[["Away", "Home", "Away Goals", "Home Goals", "Date"]].copy()
away_df.columns = ["Team", "Opponent", "Goals For", "Goals Against", "Date"]
away_df["Result"] = away_df.apply(
    lambda row: "W" if row["Goals For"] > row["Goals Against"] else "L" if row["Goals For"] < row["Goals Against"] else "D",
    axis=1
)

# Combine matches
all_matches = pd.DataFrame(columns=["Team", "Opponent", "Goals For", "Goals Against", "Date", "Result"])
if show_home:
    all_matches = pd.concat([all_matches, home_df], ignore_index=True)
if show_away:
    all_matches = pd.concat([all_matches, away_df], ignore_index=True)

# Filter matches for selected teams
# Apply round filter to df before generating tables
if selected_specific_rounds:
    all_matches = all_matches[all_matches["Date"].isin(df[df["Round"].astype(int).isin(selected_specific_rounds)]["Date"])]
else:
    all_matches = all_matches[all_matches["Date"].isin(df[df["Round"].astype(int).between(selected_round_range[0], selected_round_range[1])]["Date"])]

all_matches = all_matches[all_matches["Team"].isin(selected_teams)]

# Compute league table
@st.cache_data
def compute_league_table(matches):
    form_map = matches.sort_values(by="Date").groupby("Team")
    def result_to_dots(results):
        symbol_map = {"W": "<span style='color:green'>●</span>", "D": "<span style='color:orange'>●</span>", "L": "<span style='color:red'>●</span>"}
        return ''.join(symbol_map.get(r, '') for r in results[-5:])

    latest_results = form_map["Result"].apply(lambda x: result_to_dots(x.tolist())).reset_index(name="Form")

    table = matches.groupby("Team").agg(
        MP=("Result", "count"),
        W=("Result", lambda x: (x == "W").sum()),
        D=("Result", lambda x: (x == "D").sum()),
        L=("Result", lambda x: (x == "L").sum()),
        GF=("Goals For", "sum"),
        GA=("Goals Against", "sum")
    ).reset_index()
    table = pd.merge(table, latest_results, on="Team", how="left")
    table["GD"] = table["GF"] - table["GA"]
    table["Pts"] = table["W"] * 3 + table["D"]
    table["Pts/MP"] = (table["Pts"] / table["MP"]).round(2)
    table = table.sort_values(by=["Pts", "GD", "GF"], ascending=False).reset_index(drop=True)
    table.insert(0, "Nr.", range(1, len(table) + 1))
    return table

table = compute_league_table(all_matches)

# Tilføj klublogoer og visningsnavne
logo_map = {
    "FC Copenhagen": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8391/teamlogo.png",
    "Midtjylland": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8113/teamlogo.png",
    "Brøndby": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8595/teamlogo.png",
    "Randers": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8410/teamlogo.png",
    "AGF": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8071/teamlogo.png",
    "Silkeborg": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8415/teamlogo.png",
    "Nordsjælland": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/10202/teamlogo.png",
    "Viborg": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/9939/teamlogo.png",
    "SønderjyskE": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8487/teamlogo.png",
    "Aalborg": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8470/teamlogo.png",
    "Lyngby": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/9907/teamlogo.png",
    "Vejle BK": "https://dxugi372p6nmc.cloudfront.net/spdk/current/64x64/8231/teamlogo.png"
}
display_name_map = {
    "Midtjylland": "FC Midtjylland",
    "FC Copenhagen": "FC København",
    "Brøndby": "Brøndby IF",
    "Randers": "Randers FC",
    "Silkeborg": "Silkeborg IF",
    "Nordsjælland": "FC Nordsjælland",
    "Viborg": "Viborg FF",
    "Aalborg": "AAB",
    "Lyngby": "Lyngby BK"
}
table["Team"] = table.apply(
    lambda row: f'<img src="{logo_map[row["Team"]]}" width="40" height="40"> {display_name_map.get(row["Team"], row["Team"])}'
    if row["Team"] in logo_map else display_name_map.get(row["Team"], row["Team"]),
    axis=1
)

# Tabs: League table, Matches, Trends
tab1, tab2, tab3, tab4 = st.tabs(["📊 Ligatabel", "📅 Kampe", "📈 Udvikling", "🏆 Intern tabel"])

with tab1:
    all_optional_columns = [col for col in table.columns if col not in ["Nr.", "Team", "Pts"]]
    all_optional_columns = list(dict.fromkeys(all_optional_columns + ["Form"]))
    if "selected_optional" not in st.session_state or not set(st.session_state["selected_optional"]).issubset(set(all_optional_columns)):
        st.session_state["selected_optional"] = all_optional_columns

    selected_optional = st.multiselect(
        "Til/Fra vælg kolonner",
        options=all_optional_columns,
        default=st.session_state["selected_optional"],
        key="selected_optional"
    )
    if "Form" in selected_optional:
        selected_optional = [col for col in selected_optional if col != "Form"]
        final_columns = ["Nr.", "Team"] + selected_optional + ["Pts", "Form"]
    else:
        final_columns = ["Nr.", "Team"] + selected_optional + ["Pts"]
    table_html = table[final_columns].to_html(escape=False, index=False, classes="centered-header")
    st.markdown(table_html, unsafe_allow_html=True)

    latest_round = df["Round"].astype(int).max()
    kamp_visning = df[df["Round"].astype(int) == latest_round]
    kamp_visning = kamp_visning[(kamp_visning["Home"].isin(selected_teams)) | (kamp_visning["Away"].isin(selected_teams))]
    kamp_visning = kamp_visning.drop(columns=["League", "Day", "Time", "Attendance", "Venue", "Home Goals", "Away Goals", "Season"], errors='ignore')

    st.subheader("Seneste runde")
    kamp_visning = kamp_visning[[col for col in kamp_visning.columns if col != "Date"] + ["Date"]]
    kamp_visning_html = kamp_visning.to_html(index=False, classes="kampoversigt", justify="center")
    st.markdown(kamp_visning_html, unsafe_allow_html=True)

with tab2:
    if selected_specific_rounds:
        kamp_visning = df[df["Round"].astype(int).isin(selected_specific_rounds)]
    else:
        kamp_visning = df[df["Round"].astype(int).between(selected_round_range[0], selected_round_range[1])]

    kamp_visning = kamp_visning[(kamp_visning["Home"].isin(selected_teams)) | (kamp_visning["Away"].isin(selected_teams))]
    st.dataframe(kamp_visning.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True, height=700)

with tab3:
    st.subheader("Udvikling i placering")
    position_df = []
    rounds_to_plot = selected_specific_rounds if selected_specific_rounds else list(range(selected_round_range[0], selected_round_range[1] + 1))
    for round_num in sorted(rounds_to_plot):
        runde_kampe = df[df["Round"].astype(int) <= round_num].copy()
        home_r = runde_kampe[["Home", "Away", "Home Goals", "Away Goals"]].copy()
        home_r.columns = ["Team", "Opponent", "GF", "GA"]
        home_r["Result"] = home_r.apply(lambda x: "W" if x["GF"] > x["GA"] else "L" if x["GF"] < x["GA"] else "D", axis=1)
        away_r = runde_kampe[["Away", "Home", "Away Goals", "Home Goals"]].copy()
        away_r.columns = ["Team", "Opponent", "GF", "GA"]
        away_r["Result"] = away_r.apply(lambda x: "W" if x["GF"] > x["GA"] else "L" if x["GF"] < x["GA"] else "D", axis=1)
        match_r = pd.concat([home_r, away_r])
        tbl = match_r.groupby("Team").agg(
            MP=("Result", "count"),
            W=("Result", lambda x: (x == "W").sum()),
            D=("Result", lambda x: (x == "D").sum()),
            L=("Result", lambda x: (x == "L").sum()),
            GF=("GF", "sum"),
            GA=("GA", "sum")
        )
        tbl["GD"] = tbl["GF"] - tbl["GA"]
        tbl["Pts"] = tbl["W"] * 3 + tbl["D"]
        tbl = tbl.sort_values(by=["Pts", "GD", "GF"], ascending=False).reset_index()
        tbl["Position"] = tbl.index + 1
        tbl["Round"] = round_num
        position_df.append(tbl[["Team", "Round", "Position"]])

    position_df = pd.concat(position_df, ignore_index=True)
    position_df = position_df[position_df["Team"].isin(selected_teams)]

    chart = alt.Chart(position_df).mark_line(point=True).encode(
        x=alt.X("Round:O", title="Runde"),
        y=alt.Y("Position:Q", sort="descending", scale=alt.Scale(domain=[1, 12], reverse=True), title="Placering"),
        color="Team:N",
        tooltip=["Team", "Round", "Position"]
    ).properties(height=500)

    st.altair_chart(chart, use_container_width=True)

with tab4:
    st.subheader("Intern tabel mellem valgte hold")
    interne_kampe = all_matches[(all_matches["Team"].isin(selected_teams)) & (all_matches["Opponent"].isin(selected_teams))]
    intern_table = compute_league_table(interne_kampe)
    intern_table["Team"] = intern_table.apply(
        lambda row: f'<img src="{logo_map[row["Team"]]}" width="40" height="40"> {display_name_map.get(row["Team"], row["Team"])}'
        if row["Team"] in logo_map else display_name_map.get(row["Team"], row["Team"]),
        axis=1
    )
    intern_table_html = intern_table[["Nr.", "Team", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]].to_html(escape=False, index=False, classes="centered-header")
    st.markdown(intern_table_html, unsafe_allow_html=True)

with tab5:
    st.subheader("Akkumuleret liga")
