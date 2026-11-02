# app.py [PART 1/2] - Initialization & User Interface Controls
import sys
import os

# Force absolute system path registration for the enterprise directory structure
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import numpy as np
import pandas as pd
import time

from src.mitt_core.infrastructure.telemetry_pi import PIHistorianSimulator
from src.mitt_core.models.pca_detector import PCABioprocessDetector
from src.mitt_core.agents.engine import GroqBioprocessAgentEngine
from src.ui.components.charts import BioTwinControlCharts
from src.ui.components.status import BioTwinStatusSystem
from config.base import STATISTICAL_CONTROL_LIMITS, GOLDEN_BATCH_TARGETS, GOLDEN_BATCH_SIGMAS

# Import the decoupled enterprise notifier layer
from src.mitt_core.infrastructure.notifier import EnterpriseNotificationService

# Streamlit application layout definitions
st.set_page_config(page_title="Pfizer MITT Bio Twin Console", page_icon="🧬", layout="wide")
st.title("🧬 Bio-Twin Operational Execution Console")
st.caption("Manufacturing Intelligence & Technology Transformation Framework Layer")

# Initialize session parameters to maintain tracking registers across high-speed loops
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
    """Initializes self-contained inference adapters with zero runtime memory lag."""
    detector = PCABioprocessDetector(n_components=STATISTICAL_CONTROL_LIMITS["pca_n_components"])
    try:
        agent = GroqBioprocessAgentEngine()
    except Exception:
        agent = None
    return detector, agent

pca_detector, groq_agent = setup_runtime_detector_and_agent()
log_path = "data/processed/batch_state_audit_trail.csv"

# Sidebar interface interaction management
with st.sidebar:
    st.header("🔄 Simulation Engine Control")
    simulation_active = st.toggle(
        label="Run Active Bioprocess Stream", 
        value=True,
        help="Turn off this switch to instantly freeze all telemetry loops, charts, and logging layers."
    )
    
    st.markdown("---")
    st.header("🎛 Process Control Interface")
    if st.button("🚨 Inject Mechanical Agitation Anomaly", use_container_width="stretch"):
        st.session_state.fault_injected = True
        # Instantly clear generator cache state to force fault propagation down the pipeline
        if "telemetry_stream" in st.session_state:
            del st.session_state["telemetry_stream"]
            
    if st.button("🟢 Reset to Normal Golden Envelope Conditions", use_container_width="stretch"):
        st.session_state.fault_injected = False
        st.session_state.metrics_history = []
        st.session_state.cached_diagnostic_report = ""
        st.session_state.last_llm_call_time = 0.0
        st.session_state.last_emailed_report_time = 0.0
        if "telemetry_stream" in st.session_state:
            del st.session_state["telemetry_stream"]
        
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
# app.py [PART 2/2] - Live Telemetry Core Loops & Visualization Engines

# ⚙️ ENTERPRISE GENERATOR MEMORY STATE TRACKER & CACHE GATES
if "pi_simulator" not in st.session_state:
    st.session_state.pi_simulator = PIHistorianSimulator()

# Keep track of the active fault state used to build the generator stream
if "current_fault_state" not in st.session_state:
    st.session_state.current_fault_state = st.session_state.fault_injected

# 🔄 DYNAMIC RE-INITIALIZATION GAGE: Reset the stream cleanly if the user toggled the fault mode
if "telemetry_stream" not in st.session_state or st.session_state.current_fault_state != st.session_state.fault_injected:
    st.session_state.current_fault_state = st.session_state.fault_injected
    st.session_state.telemetry_stream = st.session_state.pi_simulator.stream_live_telemetry(
        inject_fault=st.session_state.fault_injected
    )

# Pull the next real consecutive data tick from the persistent execution buffer trace
try:
    latest_snapshot = next(st.session_state.telemetry_stream)
except (StopIteration, KeyError, ValueError):
    # Safe structural wrapper to rebuild the stream framework if data sequences clear out
    st.session_state.telemetry_stream = st.session_state.pi_simulator.stream_live_telemetry(
        inject_fault=st.session_state.fault_injected
    )
    latest_snapshot = next(st.session_state.telemetry_stream)

# --- Keep the rest of your mathematical evaluation (input_vector, pca_detector) exactly as it was ---
input_vector = np.array([[latest_snapshot.parameters[k] for k in GOLDEN_BATCH_TARGETS.keys()]])
results = pca_detector.transform_and_evaluate(input_vector)

if simulation_active:
    st.session_state.metrics_history.append({
        "timestamp": latest_snapshot.timestamp, 
        "t2_value": results["t2_value"], 
        "t2_ucl": results["t2_ucl"],
        "spe_value": results["spe_value"], 
        "spe_ucl": results["spe_ucl"]
    })

    # Synchronized with your custom 40-point buffer limit configuration boundary
    if len(st.session_state.metrics_history) > STATISTICAL_CONTROL_LIMITS["buffer_memory_limit"]:
        st.session_state.metrics_history.pop(0)

    BioTwinStatusSystem.log_process_state_to_file(latest_snapshot.parameters, results)

df_history = pd.DataFrame(st.session_state.metrics_history)

# -----------------------------------------------------------------------------
# 🔮 PREDICTIVE FORECASTING ENGINE (5-MINUTE RED ALERT LOOKAHEAD)
# -----------------------------------------------------------------------------
predictive_5min_alert = False
estimated_minutes_to_breach = None
target_metric_label = ""

# Noise-filtered moving trend window optimized for 200ms sampling ticks
if len(df_history) >= 15:
    sampling_interval = STATISTICAL_CONTROL_LIMITS.get("sampling_interval_seconds", 0.2)
    
    for val_col, ucl_col, name_str in [("t2_value", "t2_ucl", "Hotelling T²"), ("spe_value", "spe_ucl", "SPE Residual")]:
        y = df_history[val_col].values[-15:] # 15-point history slice (3 seconds lookback)
        x = np.arange(len(y)) * sampling_interval
        
        # Calculate ordinary least squares slope trajectory
        slope, _ = np.polyfit(x, y, 1)
        current_val = y[-1]
        ucl_limit = df_history[ucl_col].values[-1]
        
        # If tracking metrics are scaling upward toward the threshold line
        if slope > 0 and current_val < ucl_limit:
            remaining_gap = ucl_limit - current_val
            seconds_to_red_alert = remaining_gap / slope
            minutes_to_red_alert = seconds_to_red_alert / 60.0
            
            # Catch if the projected crash timeline sits within the 5-minute envelope
            if 0.0 < minutes_to_red_alert <= 5.0:
                predictive_5min_alert = True
                estimated_minutes_to_breach = minutes_to_red_alert
                target_metric_label = name_str
                break

active_red_alert = results["t2_alarm"] or results["spe_alarm"]

# -----------------------------------------------------------------------------
# 4. DASHBOARD RENDERING: HEADER & PARAMETERS GRID
# -----------------------------------------------------------------------------
if predictive_5min_alert and not active_red_alert:
    st.warning(f"🔮 **PREDICTIVE EMERGENCY INCOMING:** {target_metric_label} trajectory projects a Red Alert violation within **{estimated_minutes_to_breach:.1f} minutes**! Dispatching automated preventive SOP actions via decoupled notification microservice.")
else:
    BioTwinStatusSystem.render_process_status_header(results)

BioTwinStatusSystem.render_parameter_metrics_grid(latest_snapshot.parameters)

# -----------------------------------------------------------------------------
# 5. CONTROL LIMIT VISUALIZATIONS (PLOTLY CHARTS)
# -----------------------------------------------------------------------------
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    fig_t2 = BioTwinControlCharts.build_statistical_trend_chart(df_history, "t2_value", "t2_ucl", "Hotelling T² Latent Variability Metrics", "#0066CC")
    st.plotly_chart(fig_t2, use_container_width="stretch", key="chart_hotelling_t2")
with c2:
    fig_spe = BioTwinControlCharts.build_statistical_trend_chart(df_history, "spe_value", "spe_ucl", "Squared Prediction Error (SPE) Multi-Residual Trends", "#FF9900")
    st.plotly_chart(fig_spe, use_container_width="stretch", key="chart_residual_spe")

# -----------------------------------------------------------------------------
# 6. HYBRID ACTION LAYER: 1-MIN SUMMARY DIGEST & 5-MIN EMERGENCY OVERRIDE
# -----------------------------------------------------------------------------
current_time = time.time()
report_interval = STATISTICAL_CONTROL_LIMITS.get("report_interval_seconds", 60.0)

# Compute elapsed delta times for both loops
time_since_last_digest = current_time - st.session_state.last_emailed_report_time
time_since_last_llm = current_time - st.session_state.last_llm_call_time

# Setup explicit conditional triggers
is_digest_window_reached = (time_since_last_digest >= report_interval)
is_emergency_active = (active_red_alert or predictive_5min_alert)

trigger_email = False
email_mode_emergency = False

# CONDITION A: Immediate 5-Minute Predictive Anomaly Override (Bypasses 1-min timer)
if is_emergency_active:
    alarm_type_label = []
    if results["t2_alarm"]: alarm_type_label.append("Hotelling T² Active")
    if results["spe_alarm"]: alarm_type_label.append("SPE Active")
    if predictive_5min_alert and not active_red_alert: 
        alarm_type_label.append(f"{target_metric_label} Projected 5-Min Violation")
    active_label_string = " & ".join(alarm_type_label)
    
    # Allow prompt regeneration if 30s rate throttle is clear or it's a completely new emergency report
    if time_since_last_llm >= 30.0 or not st.session_state.cached_diagnostic_report:
        trigger_email = True
        email_mode_emergency = True

# CONDITION B: Routine 1-Minute Continuous Update Digest (Fires when system is steady)
elif is_digest_window_reached or not st.session_state.cached_diagnostic_report:
    active_label_string = "🟢 STABLE GOLDEN BATCH"
    trigger_email = True
    email_mode_emergency = False

# Execute centralized AI calculation and email distribution
if enable_llm_diagnostics and simulation_active and trigger_email:
    if groq_agent is not None:
        with st.spinner("Processing Hybrid Subsystem AI Diagnostics..."):
            
            # Pass parameters down to your custom prompt library overrides
            new_report = groq_agent.analyze_process_anomaly(
                snapshot=latest_snapshot, 
                statistical_metrics=results,
                time_to_breach_min=estimated_minutes_to_breach if email_mode_emergency else None
            )
            
            if "Failed to execute" not in new_report and "Rate limit reached" not in new_report:
                st.session_state.cached_diagnostic_report = new_report
                st.session_state.last_llm_call_time = current_time
                
                # Route through unified hybrid dispatch service method
                success = EnterpriseNotificationService.dispatch_hybrid_alert(
                    report_markdown=new_report,
                    alarm_type=active_label_string,
                    latest_parameters=latest_snapshot.parameters,
                    is_emergency=email_mode_emergency,
                    time_to_breach=estimated_minutes_to_breach if email_mode_emergency else None
                )
                
                if success:
                    if email_mode_emergency:
                        st.toast("🚨 IMMEDIATE 5-MIN CRITICAL OVERRIDE EMAIL DISPATCHED!")
                    else:
                        st.toast("📊 Routine 1-Minute Performance Digest Email Dispatched.")
                
                st.session_state.last_emailed_report_time = current_time
            else:
                st.error(new_report)
    else:
        st.warning("Groq Client framework offline. Configure GROQ_API_KEY environment variable token.")

# Render whatever report is currently cached in memory on the UI layout
if st.session_state.cached_diagnostic_report:
    st.info(st.session_state.cached_diagnostic_report)
    if simulation_active:
        countdown = max(0.0, report_interval - (time.time() - st.session_state.last_emailed_report_time))
        st.caption(f"⚙️ **Hybrid Monitor Engaged.** Standard 1-Min Digest refresh in: **{countdown:.1f}s**. *5-Min Predictive Interrupt Active 24/7.*")
    else:
        st.caption("⏸️ Simulation paused. Diagnostic reporting states frozen.")

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
