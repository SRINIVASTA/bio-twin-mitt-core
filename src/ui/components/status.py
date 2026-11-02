import streamlit as st
from typing import Dict


class BioTwinStatusSystem:
    @staticmethod
    def render_process_status_header(evaluation_results: Dict[str, Any]) -> None:
        t2_alarm = evaluation_results.get("t2_alarm", False)
        spe_alarm = evaluation_results.get("spe_alarm", False)

        if t2_alarm and spe_alarm:
            st.error("### 🛑 CRITICAL GxP STATUS ALARM: PROCESS SHIFT & RESIDUAL EXCURSION BREACH DETECTED")
        elif spe_alarm:
            st.warning("### ⚠️ UNMODELED DISTURBANCE OUTLIER DETECTED (SPE METRIC LIMIT EXCEEDED)")
        elif t2_alarm:
            st.warning("### 📉 KINETIC SHIFT DRIFT ALERT: ACTIVE TRAJECTORY DEVIATING FROM GOLDEN BATCH ENVELOPE")
        else:
            st.success("### 🟢 LIVE MONITORING LOG STATUS: STABLE OPERATIONAL VALIDATED STATE VERIFIED")

    @staticmethod
    def render_parameter_metrics_grid(parameters: Dict[str, float]) -> None:
        cols = st.columns(len(parameters))
        for col, (name, val) in zip(cols, parameters.items()):
            label_text = name.upper().replace("_", " ")
            unit = " °C" if "temp" in name else " RPM" if "rpm" in name else " L/min" if "air" in name or "aeration" in name else " kg/hr" if "feed" in name else ""
            col.metric(label=label_text, value=f"{val}{unit}")
