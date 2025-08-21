import streamlit as st
import pandas as pd
from supabase import create_client
import plotly.express as px

# --- Connect ke Supabase ---
url = "https://tmkmdclgtlaartfthsfl.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRta21kY2xndGxhYXJ0ZnRoc2ZsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTc2NDU4NywiZXhwIjoyMDcxMzQwNTg3fQ.AwjbKtq8dBpHQsT5eJkj9WhGkicj-HngRHt9OfwvRdA"
supabase = create_client(url, key)

# --- Query data dari tabel call_analysis ---
response = supabase.table("call_analysis").select("*").execute()
data = pd.DataFrame(response.data)

st.set_page_config(page_title="BNI Call Center Dashboard", layout="wide")

# --- Branding Header ---
st.markdown(
    "<h1 style='color:#FF6600;'>📞 BNI Call Center Dashboard</h1>", 
    unsafe_allow_html=True
)

# --- Ringkasan Harian ---
st.subheader("Ringkasan Harian")
daily_counts = data.groupby(data['created_at'].str[:10]).size().reset_index(name='jumlah')
st.line_chart(daily_counts.set_index('created_at'))

# --- Top 10 Topic ---
st.subheader("Top 10 Topic")
top_topics = data['topic'].value_counts().head(10).reset_index()
top_topics.columns = ['topic', 'jumlah']
fig = px.bar(top_topics, x='topic', y='jumlah', title="Top 10 Topic Paling Sering", 
             color_discrete_sequence=["#FF6600"])
st.plotly_chart(fig, use_container_width=True)

# --- Performa Agent ---
st.subheader("Performa Agent (Jumlah Call per Agent)")
agent_perf = data.groupby('nama_petugas_agent').size().reset_index(name='jumlah')
fig_agent = px.bar(agent_perf, x='nama_petugas_agent', y='jumlah', 
                   title="Jumlah Call per Agent", color_discrete_sequence=["#006A4D"])
st.plotly_chart(fig_agent, use_container_width=True)

# --- Tabel Detail ---
st.subheader("Detail Percakapan")
st.dataframe(data[['contact_id','nama_petugas_agent','nama_nasabah','topic','status','created_at']])
