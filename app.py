import streamlit as st
import pandas as pd
from supabase import create_client
import plotly.express as px

# ---- Setup page ----
st.set_page_config(page_title="BNI Call Center Dashboard", layout="wide")

# ---- Connect Supabase ----
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ---- Query data ----
response = supabase.table("call_analysis").select("*").execute()
data = pd.DataFrame(response.data)

# ---- Branding Header ----
st.markdown(
    "<h1 style='color:#FF6600;'>📞 BNI Call Center Dashboard</h1>",
    unsafe_allow_html=True
)

# ---- Summary Cards ----
col1, col2, col3 = st.columns(3)
col1.metric("Total Calls", len(data))
col2.metric("Resolved", (data["status"] == "resolved").sum())
col3.metric("Escalated", (data["status"] == "escalated").sum())

# ---- Daily Trend ----
st.subheader("📈 Ringkasan Harian")
if "created_at" in data.columns:
    data["created_date"] = pd.to_datetime(data["created_at"]).dt.date
    daily_counts = data.groupby("created_date").size().reset_index(name="jumlah")
    st.line_chart(daily_counts.set_index("created_date"))

# ---- Top 10 Topics ----
st.subheader("🔥 Top 10 Topic")
if "topic" in data.columns:
    top_topics = data["topic"].value_counts().head(10).reset_index()
    top_topics.columns = ["topic", "jumlah"]
    fig = px.bar(
        top_topics,
        x="topic",
        y="jumlah",
        title="Top 10 Topic Paling Sering",
        color_discrete_sequence=["#FF6600"]
    )
    st.plotly_chart(fig, use_container_width=True)

# ---- Agent Performance ----
st.subheader("👩‍💼 Performa Agent")
if "nama_petugas_agent" in data.columns:
    agent_perf = data.groupby("nama_petugas_agent").size().reset_index(name="jumlah")
    fig_agent = px.bar(
        agent_perf,
        x="nama_petugas_agent",
        y="jumlah",
        title="Jumlah Call per Agent",
        color_discrete_sequence=["#006A4D"]
    )
    st.plotly_chart(fig_agent, use_container_width=True)

# ---- Detail Table ----
st.subheader("📋 Detail Percakapan")
cols = ["contact_id", "nama_petugas_agent", "nama_nasabah", "topic", "status", "created_at"]
available_cols = [c for c in cols if c in data.columns]
st.dataframe(data[available_cols])
