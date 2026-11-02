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

# -----------------------------------------------------------------------------
# 1. STREAMLIT UI CONFIGURATION & STATE INITIALIZATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Pfizer MITT Bio Twin Console", page_icon="🧬", layout="wide")
st.title("🧬 Bio-Twin Operational Execution Console")
st.caption("Manufacturing Intelligence & Technology Transformation Framework Layer")

# Initialize session parameters to maintain tracking registers across loop cycles
if "metrics_history" not in st.session_state:
    st.session_state.metrics_history = []
if "fault_injected" not in st.session_state:
    st.session_state.fault_injected = False
if "last_llm_call_time" not in st.session_state:
    st.session_state.last_llm_call_time = 0.0
if "cached_diagnostic_report" not in st.session_state:
    st.session_state.cached_diagnostic_report = ""

@st.cache_resource
def setup_runtime_detector_and_agent():
    """Initializes self-contained inference adapters with zero runtime memory lag."""
    detector = PCABioprocessDetector(n_components=STATISTICAL_CONTROL_LIMITS["pca_n_components"])
    try:
        agent = GroqBioprocessAgentEngine()
    except Exception:
        agent = None
    return detector, agent

pca_detector, groq_agent = setup_runtime_detector_and_agent()

# Define structural path strings for files
log_path = "data/processed/batch_state_audit_trail.csv"

# -----------------------------------------------------------------------------
# 2. INTERFACE CONTROL SIDEBAR & TOGGLES
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("🔄 Simulation Engine Control")
    # Master Start / Stop Toggle Switch for the simulation execution pipeline
    simulation_active = st.toggle(
        label="Run Active Bioprocess Stream", 
        value=True,
        help="Turn off this switch to instantly freeze all telemetry loops, charts, and logging layers."
    )
    
    st.markdown("---")
    st.header("🎛 Process Control Interface")
    if st.button("🚨 Inject Mechanical Agitation Anomaly", use_container_width="stretch"):
        st.session_state.fault_injected = True
    if st.button("🟢 Reset to Normal Golden Envelope Conditions", use_container_width="stretch"):
        st.session_state.fault_injected = False
        st.session_state.metrics_history = []
        st.session_state.cached_diagnostic_report = ""
        st.session_state.last_llm_call_time = 0.0
        
    st.markdown("---")
    st.header("🤖 AI Agent Settings")
    enable_llm_diagnostics = st.checkbox(
        label="Enable Groq LLM Analysis", 
        value=True,
        help="Uncheck this box to pause automated LLM diagnostic requests during active process alarms."
    )

    st.markdown("---")
    st.header("📥 Data Export Options")
    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
        try:
            df_download = pd.read_csv(log_path)
            csv_bytes = df_download.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Audit Log CSV",
                data=csv_bytes,
                file_name="batch_state_audit_trail.csv",
                mime="text/csv",
                use_container_width="stretch"
            )
        except Exception:
            st.caption("Preparing data stream download channels...")
    else:
        st.caption("Awaiting process telemetry to generate download file structure.")

    st.markdown("---")
    st.header("🧹 Cache & Log Management")
    if st.button("🗑️ Clear Local Audit Log & Cache", use_container_width="stretch"):
        st.session_state.metrics_history = []
        st.session_state.cached_diagnostic_report = ""
        st.session_state.last_llm_call_time = 0.0
        st.session_state.fault_injected = False
        if os.path.exists(log_path):
            try:
                os.remove(log_path)
                st.success("Successfully deleted local historical audit file.")
            except Exception as e:
                st.error(f"File erase locked: {str(e)}")
        st.cache_resource.clear()
        st.toast("Wiped application context caches clean!")
        time.sleep(1.0)
        st.rerun()

# -----------------------------------------------------------------------------
# 3. TELEMETRY STREAM ACQUISITION & STATISTICAL ANALYSIS
# -----------------------------------------------------------------------------
simulator = PIHistorianSimulator()
stream = simulator.stream_live_telemetry(inject_fault=st.session_state.fault_injected)
latest_snapshot = next(stream)

# Build features matrix matching config order
input_vector = np.array([[latest_snapshot.parameters[k] for k in GOLDEN_BATCH_TARGETS.keys()]])

# Execute high-speed statistical control evaluation checks
results = pca_detector.transform_and_evaluate(input_vector)

# Track values over time for dashboard visualization charts only if simulation is actively running
if simulation_active:
    st.session_state.metrics_history.append({
        "timestamp": latest_snapshot.timestamp, 
        "t2_value": results["t2_value"], 
        "t2_ucl": results["t2_ucl"],
        "spe_value": results["spe_value"], 
        "spe_ucl": results["spe_ucl"]
    })

    if len(st.session_state.metrics_history) > STATISTICAL_CONTROL_LIMITS["buffer_memory_limit"]:
        st.session_state.metrics_history.pop(0)

    # Automatically saves the historical row tracking states down into your local data folder
    BioTwinStatusSystem.log_process_state_to_file(latest_snapshot.parameters, results)

df_history = pd.DataFrame(st.session_state.metrics_history)

# -----------------------------------------------------------------------------
# 4. DASHBOARD RENDERING: HEADER & PARAMETERS GRID
# -----------------------------------------------------------------------------
BioTwinStatusSystem.render_process_status_header(results)
BioTwinStatusSystem.render_parameter_metrics_grid(latest_snapshot.parameters)

# -----------------------------------------------------------------------------
# 5. CONTROL LIMIT VISUALIZATIONS (PLOTLY CHARTS)
# -----------------------------------------------------------------------------
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    fig_t2 = BioTwinControlCharts.build_statistical_trend_chart(df_history, "t2_value", "t2_ucl", "Hotelling T² Latent Variability Metrics", "#0066CC")
    st.plotly_chart(fig_t2, use_container_width="stretch")
with c2:
    fig_spe = BioTwinControlCharts.build_statistical_trend_chart(df_history, "spe_value", "spe_ucl", "Squared Prediction Error (SPE) Multi-Residual Trends", "#FF9900")
    st.plotly_chart(fig_spe, use_container_width="stretch")

# -----------------------------------------------------------------------------
# 6. AGENTIC AI DECISION-SUPPORT LAYER WITH API THROTTLING GUARD
# -----------------------------------------------------------------------------
if results["t2_alarm"] or results["spe_alarm"]:
    st.markdown("### 🤖 Groq Autonomous LLM Diagnostic Hub")
    
    if enable_llm_diagnostics:
        current_time = time.time()
        time_elapsed_since_last_call = current_time - st.session_state.last_llm_call_time
        
        # Only call the LLM if the simulation is active to prevent static infinite loops
        if simulation_active and (time_elapsed_since_last_call > 30.0 or not st.session_state.cached_diagnostic_report):
            if groq_agent is not None:
                with st.spinner("Invoking low-latency diagnostic calculation steps..."):
                    new_report = groq_agent.analyze_process_anomaly(latest_snapshot, results)
                    
                    if "Failed to execute" not in new_report and "Rate limit reached" not in new_report:
                        st.session_state.cached_diagnostic_report = new_report
                        st.session_state.last_llm_call_time = current_time
                    else:
                        st.error(new_report)
            else:
                st.warning("Groq Client framework offline. Configure GROQ_API_KEY environment variable token.")
        
        if st.session_state.cached_diagnostic_report:
            st.info(st.session_state.cached_diagnostic_report)
            if simulation_active:
                st.caption(f"⏱️ Diagnostic report locked. Next token window refresh available in: {max(0.0, 30.0 - time_elapsed_since_last_call):.1f}s")
            else:
                st.caption("⏸️ Simulation paused. Diagnostic state frozen.")
    else:
        st.caption("LLM Analysis is currently paused via the sidebar toggle checkbox control.")

# -----------------------------------------------------------------------------
# 7. HISTORICAL BATCH AUDIT FILE VIEWER LAYER
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("📋 Historical Batch Audit File Viewer (`data/processed/`)")

if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
    try:
        df_audit = pd.read_csv(log_path)
        st.dataframe(df_audit.tail(15), use_container_width="stretch")
    except Exception:
        st.caption("Refreshing data log file registers...")
else:
    st.caption("Awaiting initial file generation sequences. System loop logging is running silently.")

# -----------------------------------------------------------------------------
# 8. RERUN LOOP OR FREEZE CONTROL
# -----------------------------------------------------------------------------
if simulation_active:
    time.sleep(STATISTICAL_CONTROL_LIMITS["sampling_interval_seconds"])
    st.rerun()
else:
    st.info("⏸️ Bioprocess stream engine is currently frozen. Turn on the switch in the sidebar to resume.")
