import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

from src.mitt_core.infrastructure.telemetry_pi import PIHistorianSimulator
from src.mitt_core.models.pca_detector import PCABioprocessDetector
from src.mitt_core.agents.engine import GroqBioprocessAgentEngine

# -----------------------------------------------------------------------------
# 1. STREAMLIT UI CONFIGURATION & STATE INITIALIZATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pfizer MITT - Bio-Twin Console", 
    page_icon="🧬", 
    layout="wide"
)

st.title("🧬 Bio-Twin Operational Execution Console")
st.subheader("Manufacturing Intelligence & Technology Transformation (MITT)")

# Initialize session storage arrays for tracking real-time metric trends
if "metrics_history" not in st.session_state:
    st.session_state.metrics_history = []
if "fault_injected" not in st.session_state:
    st.session_state.fault_injected = False

# -----------------------------------------------------------------------------
# 2. CACHED ENGINE & REFERENCE DATA INITIALIZATION
# -----------------------------------------------------------------------------
@st.cache_resource
def initialize_analytics_engines():
    """
    Simulates historical training matrices from reference runs to fit the 
    PCA soft-sensor and initializes the Groq LLM client infrastructure.
    """
    # Generate mock training dataset representing stable golden batch runs
    # Order: [temperature, ph, agitation_rpm, aeration_rate, substrate_feed_rate]
    np.random.seed(42)
    normal_data = np.random.normal(
        loc=[25.0, 6.5, 120.0, 250.0, 0.50],
        scale=[0.1, 0.02, 1.5, 2.0, 0.01],
        size=(200, 5)
    )
    
    # Fit the Latent Variable Anomaly Detector
    detector = PCABioprocessDetector(n_components=2, alpha=0.05)
    detector.fit(normal_data)
    
    # Initialize Groq Engine (Will gracefully fall back to errors if credentials lack)
    try:
        agent = GroqBioprocessAgentEngine()
    except Exception:
        agent = None
        
    return detector, agent

pca_detector, groq_agent = initialize_analytics_engines()

# -----------------------------------------------------------------------------
# 3. INTERFACE CONTROL SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("🎛 Process Control Interface")
    st.markdown("Interact with the live running bioreactor stream simulation layer.")
    
    # Button allowing active injection of process degradation states
    if st.button("🚨 Inject Mechanical Agitation Anomaly", use_container_width=True):
        st.session_state.fault_injected = True
        st.warning("Process fault matrix actively injected into stream.")
        
    if st.button("🟢 Reset to Normal Golden Batch Conditions", use_container_width=True):
        st.session_state.fault_injected = False
        st.session_state.metrics_history = []
        st.success("Cleared historical registers and normalized streams.")

# -----------------------------------------------------------------------------
# 4. TELEMETRY STREAM ACQUISITION
# -----------------------------------------------------------------------------
simulator = PIHistorianSimulator(batch_id="BATCH-2026-MITT")
stream_generator = simulator.stream_live_telemetry(
    interval_seconds=0.1, 
    inject_fault=st.session_state.fault_injected
)

# Pull the latest single data frame snapshot from the historian pipeline
latest_snapshot = next(stream_generator)

# Extract vector fields for the PCA transformation pipeline
input_vector = np.array([[
    latest_snapshot.parameters["temperature"],
    latest_snapshot.parameters["ph"],
    latest_snapshot.parameters["agitation_rpm"],
    latest_snapshot.parameters["aeration_rate"],
    latest_snapshot.parameters["substrate_feed_rate"]
]])

# Execute inference via the statistical process control matrix
results = pca_detector.transform_and_evaluate(input_vector)

# Store the output record inside historical trends array
st.session_state.metrics_history.append({
    "timestamp": latest_snapshot.timestamp,
    "agitation_rpm": latest_snapshot.parameters["agitation_rpm"],
    "t2_value": results["t2_value"],
    "t2_ucl": results["t2_ucl"],
    "spe_value": results["spe_value"],
    "spe_ucl": results["spe_ucl"]
})

# Restrict local session memory buffer size to avoid frontend browser bloating
if len(st.session_state.metrics_history) > 40:
    st.session_state.metrics_history.pop(0)

df_history = pd.DataFrame(st.session_state.metrics_history)

# -----------------------------------------------------------------------------
# 5. LIVE METRICS & PLOTLY DASHBOARD RENDERING
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧪 Active Batch", latest_snapshot.batch_id)
col2.metric("⏱ Age (Hours)", f"{latest_snapshot.step_duration_hours:.4f} hrs")
col3.metric(
    "🌀 Agitation Rate", 
    f"{latest_snapshot.parameters['agitation_rpm']:.1f} RPM",
    delta=f"{latest_snapshot.parameters['agitation_rpm'] - 120.0:.1f} vs Ref"
)
col4.metric(
    "📊 Sensor Health Check", 
    "ALARM ACTIVE" if (results["t2_alarm"] or results["spe_alarm"]) else "STABLE (GxP)",
    delta="CRITICAL" if results["spe_alarm"] else "NORMAL",
    delta_color="inverse" if (results["t2_alarm"] or results["spe_alarm"]) else "normal"
)

# Build real-time Hotelling T-squared tracking graph
fig_t2 = go.Figure()
fig_t2.add_trace(go.Scatter(x=df_history.index, y=df_history["t2_value"], name="Hotelling T²", line=dict(color="#0066CC")))
fig_t2.add_trace(go.Scatter(x=df_history.index, y=df_history["t2_ucl"], name="T² UCL Limit", line=dict(color="red", dash="dash")))
fig_t2.update_layout(title="Hotelling T² Latent Space Variation Trends", template="plotly_dark", height=300, margin=dict(l=20, r=20, t=40, b=20))

# Build real-time SPE Q-Residual tracking graph
fig_spe = go.Figure()
fig_spe.add_trace(go.Scatter(x=df_history.index, y=df_history["spe_value"], name="SPE (Q)", line=dict(color="#FF9900")))
fig_spe.add_trace(go.Scatter(x=df_history.index, y=df_history["spe_ucl"], name="SPE UCL Limit", line=dict(color="red", dash="dash")))
fig_spe.update_layout(title="Squared Prediction Error (SPE) Residual Trends", template="plotly_dark", height=300, margin=dict(l=20, r=20, t=40, b=20))

chart_col1, chart_col2 = st.columns(2)
chart_col1.plotly_chart(fig_t2, use_container_width=True)
chart_col2.plotly_chart(fig_spe, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. AGENTIC AI DECISION-SUPPORT LAYER
# -----------------------------------------------------------------------------
st.divider()
st.subheader("🤖 Groq Autonomous LLM Diagnostic Hub")

if results["t2_alarm"] or results["spe_alarm"]:
    st.error("⚠️ Multi-variable control parameters have breached safe GxP operation boundaries.")
    
    if groq_agent is not None:
        with st.spinner("Submitting telemetry packet to Groq low-latency inference cluster..."):
            diagnostic_report = groq_agent.analyze_process_anomaly(latest_snapshot, results)
            st.markdown("### Actionable SOP Diagnostic Summary:")
            st.info(diagnostic_report)
    else:
        st.warning(
            "Groq Client infrastructure inactive. Add a valid `GROQ_API_KEY` to your environment or "
            "`.streamlit/secrets.toml` config layer to receive automated root-cause reports."
        )
else:
    st.success("🟢 Continuous monitoring profile reveals all variables remain locked within Golden Batch limits.")

# Force Streamlit to instantly re-execute and query the loop generator for immediate UI refreshes
st.rerun()
