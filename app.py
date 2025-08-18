import time
import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "data/stream.db"
REFRESH_S = 3  

st.set_page_config(page_title="Last-Mile KPI", layout="wide")
st.title("Last-Mile KPI (SQLite)")

# ---- staattiset jutut (suodattimet yms) renderöidään kerran -----------------
@st.cache_data  # ei ttl:tä; päivitämme datan erikseen “livenä” alempana
def load_all():
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM deliveries", con)
    con.close()
    return df

df_all = load_all()

# Suodattimet pysyy paikallaan (ei rerunia)
cols = st.columns(3)
area = cols[0].selectbox("Area", ["(all)"] + sorted(df_all["Area"].dropna().unique().tolist()))
veh  = cols[1].selectbox("Vehicle", ["(all)"] + sorted(df_all["Vehicle"].dropna().unique().tolist()))
wthr = cols[2].selectbox("Weather", ["(all)"] + sorted(df_all["Weather"].dropna().unique().tolist()))

def apply_filters(df):
    if area != "(all)":
        df = df[df["Area"] == area]
    if veh != "(all)":
        df = df[df["Vehicle"] == veh]
    if wthr != "(all)":
        df = df[df["Weather"] == wthr]
    return df

# ---- varaa paikat osioille joita päivitetään "livenä" ----------------------
kpi_ph   = st.empty()
pivot_ph = st.empty()
hist_ph  = st.empty()
risk_ph  = st.empty()
map_ph   = st.empty()
tail_ph  = st.empty()

# Live-tila päälle/pois (ei rerunia – looppi hoitaa päivitykset)
live = st.toggle("Live-päivitys", value=True)

def render_once():
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM deliveries", con)
    con.close()

    # tyypitys
    for c in ["Delivery_Time", "Agent_Rating"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df = apply_filters(df)

    # KPI
    with kpi_ph.container():
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Tilauksia", len(df))
        if "Delivery_Time" in df and df["Delivery_Time"].notna().any():
            c2.metric("Keski (min)", f"{df['Delivery_Time'].mean():.1f}")
            c3.metric("P90 (min)",   f"{df['Delivery_Time'].quantile(0.90):.1f}")
        if "Agent_Rating" in df and df["Agent_Rating"].notna().any():
            c4.metric("Keskim. rating", f"{df['Agent_Rating'].mean():.2f}")

    # Pivot
    with pivot_ph.container():
        st.subheader("Area × Traffic (keskimääräinen toimitusaika, min)")
        if {"Area","Traffic","Delivery_Time"}.issubset(df.columns):
            pt = df.pivot_table(values="Delivery_Time", index="Area", columns="Traffic", aggfunc="mean").round(1)
            st.dataframe(pt, use_container_width=True)

    # Jakauma
    with hist_ph.container():
        st.subheader("Toimitusaikojen jakauma")
        if "Delivery_Time" in df:
            st.bar_chart(df["Delivery_Time"].dropna())

    # Riskit
    with risk_ph.container():
        if {"Area","Traffic","Weather","Delivery_Time"}.issubset(df.columns):
            p90 = df.groupby("Area")["Delivery_Time"].quantile(0.90)
            df2 = df.join(p90, on="Area", rsuffix="_p90")
            df2["Late_Risk"] = ((df2["Delivery_Time"] > df2["Delivery_Time_p90"]) |
                                (df2["Traffic"].isin(["High","Jam"]) &
                                 df2["Weather"].isin(["Stormy","Sandstorms"]))).astype(int)
            st.subheader("Myöhästymisriskin jakauma")
            st.bar_chart(df2["Late_Risk"].value_counts())

    # Kartta
    with map_ph.container():
        st.subheader("Drop-off sijainnit kartalla (viimeiset 300 riviä)")
        LAT_COL, LON_COL = "Drop_Latitude", "Drop_Longitude"
        if {LAT_COL,LON_COL}.issubset(df.columns):
            m = df.sort_values("id").tail(300)[[LAT_COL,LON_COL]].copy()
            for c in [LAT_COL, LON_COL]:
                m[c] = m[c].astype(str).str.replace(",", ".", regex=False).pipe(pd.to_numeric, errors="coerce")
            m = m.dropna()
            m = m[m[LAT_COL].between(-90,90) & m[LON_COL].between(-180,180)]
            if not m.empty:
                st.map(m.rename(columns={LAT_COL:"lat", LON_COL:"lon"})[["lat","lon"]])

    # Viimeiset rivit
    with tail_ph.container():
        st.subheader("Viimeiset rivit")
        st.dataframe(df.sort_values("id", ascending=False).head(20), use_container_width=True)

# Päivitä vain nämä placeholderit – ei koko sivua
if live:
    # tee muutama sykli; Streamlit ei pidä äärettömistä loopeista
    for _ in range(999999):
        render_once()
        time.sleep(REFRESH_S)
else:
    render_once()
