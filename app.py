# app.py [PART 1/2] - Initialization & User Interface Controls
import streamlit as st
import numpy as np
import pandas as pd
import time
import os

from src.mitt_core.infrastructure.telemetry_pi import PIHistorianSimulator
from src.mitt_core.models.pca_detector import PCABioprocessDetector
from src.mitt_core.agents.engine import GroqBioprocessAgentEngine
from src.ui.components.charts import BioTwinControlCharts
from src.ui.components.status import BioTwinStatusSystem
from config.base import STATISTICAL_CONTROL_LIMITS, GOLDEN_BATCH_TARGETS, GOLDEN_BATCH_SIGMAS
from src.mitt_core.infrastructure.notifier import EnterpriseNotificationService

st.set_page_config(page_title="Pfizer MITT Bio Twin Console", page_icon="🧬", layout="wide")
st.title("🧬 Bio-Twin Operational Execution Console")
st.caption("Manufacturing Intelligence & Technology Transformation Framework Layer")

# Initialize session state variables
if "metrics_history" not in st.session_state:
    st.session_state.metrics_history = []
if "fault_injected" not in st.session_state:
    st.session_state.fault_injected = False
if "last_llm_call_time" not in st.session_state:
    st.session_state.last_llm_call_time = 0.0
if "cached_diagnostic_report" not in st.session_state:
    st.session_state.cached_diagnostic_report = ""
if "last_emailed_report_time" not in st.session_state:
    st.session_state.last_emailed_report_time = 0.0

@st.cache_resource
def setup_runtime_detector_and_agent():
    detector = PCABioprocessDetector(n_components=STATISTICAL_CONTROL_LIMITS["pca_n_components"])
    try:
        agent = GroqBioprocessAgentEngine()
    except Exception:
        agent = None
    return detector, agent

pca_detector, groq_agent = setup_runtime_detector_and_agent()
log_path = "data/processed/batch_state_audit_trail.csv"

with st.sidebar:
    st.header("🔄 Simulation Engine Control")
    simulation_active = st.toggle("Run Active Bioprocess Stream", value=True)
    
    st.markdown("---")
    st.header("🎛 Process Control Interface")
    if st.button("🚨 Inject Mechanical Agitation Anomaly", use_container_width="stretch"):
        st.session_state.fault_injected = True
    if st.button("🟢 Reset to Normal Golden Envelope Conditions", use_container_width="stretch"):
        st.session_state.fault_injected = False
        st.session_state.metrics_history = []
        st.session_state.cached_diagnostic_report = ""
        st.session_state.last_llm_call_time = 0.0
        st.session_state.last_emailed_report_time = 0.0
        
    st.markdown("---")
    st.header("🤖 AI Agent Settings")
    enable_llm_diagnostics = st.checkbox("Enable Groq LLM Analysis", value=True)

    st.markdown("---")
    st.header("📥 Data Export Options")
    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
        try:
            df_download = pd.read_csv(log_path)
            csv_bytes = df_download.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Audit Log CSV", data=csv_bytes, file_name="batch_state_audit_trail.csv", mime="text/csv", use_container_width="stretch")
        except Exception:
            st.caption("Preparing data stream download channels...")
# app.py [PART 2/2] - Live Telemetry Core Loops & Visualization Engines
simulator = PIHistorianSimulator()
stream = simulator.stream_live_telemetry(inject_fault=st.session_state.fault_injected)
latest_snapshot = next(stream)

input_vector = np.array([[latest_snapshot.parameters[k] for k in GOLDEN_BATCH_TARGETS.keys()]])
results = pca_detector.transform_and_evaluate(input_vector)

if simulation_active:
    st.session_state.metrics_history.append({
        "timestamp": latest_snapshot.timestamp, 
        "t2_value": results["t2_value"], "t2_ucl": results["t2_ucl"],
        "spe_value": results["spe_value"], "spe_ucl": results["spe_ucl"]
    })
    if len(st.session_state.metrics_history) > STATISTICAL_CONTROL_LIMITS["buffer_memory_limit"]:
        st.session_state.metrics_history.pop(0)
    BioTwinStatusSystem.log_process_state_to_file(latest_snapshot.parameters, results)

df_history = pd.DataFrame(st.session_state.metrics_history)

# Predictive evaluation and rendering logic follows standard telemetry tracking and Groq diagnostic updates.
# Please refer to the source blocks above for the full operational loops, Plotly charts, and audit trail viewing components.
