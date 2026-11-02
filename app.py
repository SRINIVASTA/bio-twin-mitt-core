import streamlit as st
import numpy as np
import pandas as pd

from src.mitt_core.infrastructure.telemetry_pi import PIHistorianSimulator
from src.mitt_core.models.pca_detector import PCABioprocessDetector
from src.mitt_core.agents.engine import GroqBioprocessAgentEngine
from src.ui.components.charts import BioTwinControlCharts
from src.ui.components.status import BioTwinStatusSystem
from config.base import STATISTICAL_CONTROL_LIMITS, GOLDEN_BATCH_TARGETS, GOLDEN_BATCH_SIGMAS

st.set_page_config(page_title="Pfizer MITT Bio Twin Console", page_icon="🧬", layout="wide")
st.title("🧬 Bio-Twin Operational Execution Console")
st.caption("Manufacturing Intelligence & Technology Transformation Framework Layer")

if "metrics_history" not in st.session_state:
    st.session_state.metrics_history = []
if "fault_injected" not in st.session_state:
    st.session_state.fault_injected = False

@st.cache_resource
def setup_runtime_detector_and_agent():
    np.random.seed(42)
    reference_data = np.random.normal(
        loc=list(GOLDEN_BATCH_TARGETS.values()),
        scale=list(GOLDEN_BATCH_SIGMAS.values()),
        size=(150, 5)
    )
    detector = PCABioprocessDetector(n_components=STATISTICAL_CONTROL_LIMITS["pca_n_components"])
    detector.fit(reference_data)
    try:
        agent = GroqBioprocessAgentEngine()
    except Exception:
        agent = None
    return detector, agent

pca_detector, groq_agent = setup_runtime_detector_and_agent()

with st.sidebar:
    st.header("🎛 Process Control Interface")
    # Updated to width='stretch' to meet API compliance rules
    if st.button("🚨 Inject Mechanical Agitation Anomaly", width='stretch'):
        st.session_state.fault_injected = True
    if st.button("🟢 Reset to Normal Golden Envelope Conditions", width='stretch'):
        st.session_state.fault_injected = False
        st.session_state.metrics_history = []

# Telemetry acquisition stream loop segment execution blocks
simulator = PIHistorianSimulator()
stream = simulator.stream_live_telemetry(inject_fault=st.session_state.fault_injected)
latest_snapshot = next(stream)

input_vector = np.array([[latest_snapshot.parameters[k] for k in GOLDEN_BATCH_TARGETS.keys()]])
results = pca_detector.transform_and_evaluate(input_vector)

st.session_state.metrics_history.append({
    "timestamp": latest_snapshot.timestamp, "t2_value": results["t2_value"], "t2_ucl": results["t2_ucl"],
    "spe_value": results["spe_value"], "spe_ucl": results["spe_ucl"]
})
if len(st.session_state.metrics_history) > STATISTICAL_CONTROL_LIMITS["buffer_memory_limit"]:
    st.session_state.metrics_history.pop(0)

df_history = pd.DataFrame(st.session_state.metrics_history)

# Component screen layout execution
BioTwinStatusSystem.render_process_status_header(results)
BioTwinStatusSystem.render_parameter_metrics_grid(latest_snapshot.parameters)

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(BioTwinControlCharts.build_statistical_trend_chart(df_history, "t2_value", "t2_ucl", "Hotelling T² Latent Variability Metrics", "#0066CC"), width='stretch')
with c2:
    st.plotly_chart(BioTwinControlCharts.build_statistical_trend_chart(df_history, "spe_value", "spe_ucl", "Squared Prediction Error (SPE) Multi-Residual Trends", "#FF9900"), width='stretch')

if results["t2_alarm"] or results["spe_alarm"]:
    st.markdown("### 🤖 Groq Autonomous LLM Diagnostic Hub")
    if groq_agent is not None:
        with st.spinner("Invoking low-latency diagnostic calculation steps..."):
            st.info(groq_agent.analyze_process_anomaly(latest_snapshot, results))
    else:
        st.warning("Groq Client framework offline. Configure GROQ_API_KEY environment variable token to populate this data feed.")

time_delay = STATISTICAL_CONTROL_LIMITS["sampling_interval_seconds"]
import time
time.sleep(time_delay)
st.rerun()
