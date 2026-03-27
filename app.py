import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="HOSDT | Clinic Command Center", layout="wide")

# Updated CSS: Fixed visibility by setting explicit text colors for metrics
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* Style the metric cards for better visibility */
    [data-testid="stMetricValue"] {
        color: #1c3d5a !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #495057 !important;
        font-size: 1rem !important;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    div[data-testid="stExpander"] { border: none !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05); background: white; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA GENERATION ENGINE ---
class ClinicSimulator:
    def __init__(self, num_patients=40, dr_speed=1.0, pharm_prob=0.6):
        self.num_patients = num_patients
        self.dr_speed = dr_speed  # 1.0 = normal, 0.5 = slow, 1.5 = fast
        self.pharm_prob = pharm_prob
        self.names = ["James Wilson", "Maria Garcia", "Robert Chen", "Sarah Miller", "Ahmed Khan", 
                      "Elena Rossi", "David Smith", "Linda Brown", "Kevin Kumar", "Sophie Dubois",
                      "John Doe", "Jane Smith", "Michael Jordan", "Emma Watson", "Chris Evans"]

    def generate_data(self):
        data = []
        # Start day at 09:00 AM
        start_of_day = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        current_arrival_time = start_of_day
        dr_free_at = start_of_day
        
        for i in range(self.num_patients):
            # 1. Arrival Logic (Randomized with Peak Hour bias)
            hour = current_arrival_time.hour
            if (10 <= hour <= 12) or (16 <= hour <= 18):
                arrival_gap = random.randint(3, 12)
            else:
                arrival_gap = random.randint(12, 35)
            
            arrival_time = current_arrival_time + timedelta(minutes=arrival_gap)
            current_arrival_time = arrival_time
            
            # 2. Patient Demographics
            p_name = random.choice(self.names) + f" {random.randint(100,999)}"
            age = int(np.random.normal(45, 18))
            age = max(5, min(95, age))
            is_new = random.random() < 0.3
            
            # 3. Registration Time
            reg_base = 8 if is_new else 2
            age_factor = 2 if age > 65 else 0
            reg_duration = random.randint(reg_base, reg_base + 5) + age_factor
            reg_end_time = arrival_time + timedelta(minutes=reg_duration)
            
            # 4. Wait & Consultation Logic
            consult_start = max(reg_end_time, dr_free_at)
            wait_time = (consult_start - reg_end_time).total_seconds() / 60
            
            consult_duration = int(np.random.normal(18, 6) / self.dr_speed)
            consult_duration = max(8, consult_duration)
            consult_end = consult_start + timedelta(minutes=consult_duration)
            dr_free_at = consult_end
            
            # 5. Financials
            base_fee = 800 if is_new else 500
            pharmacy_visit = random.random() < (self.pharm_prob + (0.15 if age > 60 or consult_duration > 20 else 0))
            pharm_spend = random.randint(450, 5500) if pharmacy_visit else 0
            
            data.append({
                "Patient ID": f"P-{1000+i}",
                "Name": p_name,
                "Age": age,
                "Type": "New" if is_new else "Returning",
                "Arrival Time": arrival_time.strftime("%H:%M"),
                "Reg Duration (min)": reg_duration,
                "Doc Entry Time": consult_start.strftime("%H:%M"),
                "Wait Duration (min)": round(wait_time, 1),
                "Consult Duration (min)": consult_duration,
                "Pharmacy Spend": pharm_spend,
                "Total Revenue": base_fee + pharm_spend,
                "Total Time in Clinic (min)": round((consult_end - arrival_time).total_seconds() / 60, 1),
                "Hour": arrival_time.hour
            })
            
        return pd.DataFrame(data)

# --- DASHBOARD UI ---
st.title("🏥 HOSDT: Single-Doctor Clinic Operations")
st.subheader("Operational Transparency & Performance Dashboard")

# Sidebar Controls
with st.sidebar:
    st.header("Simulation Settings")
    patient_count = st.slider("Daily Patients", 10, 100, 40)
    doc_efficiency = st.select_slider("Doctor Work Pace", options=[0.5, 1.0, 1.5, 2.0], value=1.0)
    pharm_rate = st.slider("Pharmacy Conversion Baseline", 0.0, 1.0, 0.5)
    
    if st.button("🔄 Regenerate Day", use_container_width=True):
        st.cache_data.clear()

# Generate Data
sim = ClinicSimulator(num_patients=patient_count, dr_speed=doc_efficiency, pharm_prob=pharm_rate)
df = sim.generate_data()

# --- KPI TILES ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Patients", len(df))
with m2:
    avg_wait = df["Wait Duration (min)"].mean()
    st.metric("Avg Wait Time", f"{avg_wait:.1f}m", delta=f"{avg_wait-15:.1f}m", delta_color="inverse")
with m3:
    total_rev = df["Total Revenue"].sum()
    st.metric("Total Revenue", f"₹{total_rev:,}")
with m4:
    avg_age = df["Age"].mean()
    st.metric("Avg Patient Age", f"{int(avg_age)} yrs")

# --- DASHBOARD TABS ---
tab_ops, tab_fin, tab_ledger = st.tabs(["🕒 Flow & Bottlenecks", "💸 Revenue Insights", "📑 Detailed Ledger"])

with tab_ops:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.write("#### Hourly Traffic Density")
        hourly_counts = df.groupby("Hour").size().reset_index(name="Patients")
        fig_vol = px.area(hourly_counts, x="Hour", y="Patients", markers=True, 
                         color_discrete_sequence=['#1f77b4'], title="Patient Arrivals per Hour")
        st.plotly_chart(fig_vol, use_container_width=True)
        
    with c2:
        st.write("#### Patient Flow Dynamics")
        fig_wait = px.scatter(df, x="Consult Duration (min)", y="Wait Duration (min)", 
                             color="Age", size="Total Revenue", hover_data=["Name", "Doc Entry Time"],
                             title="Wait Time vs Consult Length")
        st.plotly_chart(fig_wait, use_container_width=True)

    st.write("#### Service Efficiency Timeline")
    fig_line = go.Figure()
    fig_line.add_trace(go.Bar(x=df.index, y=df["Reg Duration (min)"], name="Reg Time", marker_color='#FFA07A'))
    fig_line.add_trace(go.Bar(x=df.index, y=df["Wait Duration (min)"], name="Wait Time", marker_color='#FF4B4B'))
    fig_line.add_trace(go.Bar(x=df.index, y=df["Consult Duration (min)"], name="Consultation", marker_color='#00CC96'))
    fig_line.update_layout(barmode='stack', title="Component Breakdown per Patient", xaxis_title="Patient Sequence")
    st.plotly_chart(fig_line, use_container_width=True)

with tab_fin:
    f1, f2 = st.columns(2)
    with f1:
        st.write("#### Revenue Sources")
        pharm_total = df["Pharmacy Spend"].sum()
        consult_total = total_rev - pharm_total
        rev_df = pd.DataFrame({"Source": ["Consultation Fees", "Pharmacy Sales"], "Value": [consult_total, pharm_total]})
        fig_rev = px.pie(rev_df, values='Value', names='Source', hole=0.5, 
                        color_discrete_sequence=['#1c3d5a', '#5ba300'])
        st.plotly_chart(fig_rev, use_container_width=True)
        
    with f2:
        st.write("#### Pharmacy Spend by Age Group")
        df['Age Group'] = pd.cut(df['Age'], bins=[0, 18, 40, 60, 100], labels=['Youth', 'Adult', 'Middle-Age', 'Senior'])
        fig_age_rev = px.box(df, x="Age Group", y="Pharmacy Spend", color="Age Group", points="all")
        st.plotly_chart(fig_age_rev, use_container_width=True)

with tab_ledger:
    st.write("#### Complete Patient Event Log")
    st.dataframe(df.drop(columns=['Hour', 'Age Group'], errors='ignore'), use_container_width=True, height=500)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button("📂 Export Log as CSV", data=csv_data, file_name=f"clinic_report_{datetime.now().strftime('%Y%m%d')}.csv")

# Footer
st.markdown("---")
st.caption(f"HOSDT Terminal | Last Simulation Sync: {datetime.now().strftime('%H:%M:%S')} | Environment: GitHub Codespaces")