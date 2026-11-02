import streamlit as st
import os
import pandas as pd
from datetime import datetime
from typing import Dict, Any


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

    @staticmethod
    def log_process_state_to_file(parameters: Dict[str, float], evaluation_results: Dict[str, Any]) -> None:
        """
        Appends historical data ticks directly to an offline batch file log,
        flagging exactly when a breach happens vs when a batch runs inside the golden envelope.
        """
        log_dir = "data/processed"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "batch_state_audit_trail.csv")

        t2_alarm = evaluation_results.get("t2_alarm", False)
        spe_alarm = evaluation_results.get("spe_alarm", False)

        # Classify the operational state deterministically
        if t2_alarm and spe_alarm:
            current_state = "CRITICAL_DUAL_BREACH"
        elif spe_alarm:
            current_state = "UNMODELED_DISTURBANCE_SPE"
        elif t2_alarm:
            current_state = "KINETIC_TRAJECTORY_SHIFT_T2"
        else:
            current_state = "GOLDEN_ENVELOPE_VALIDATED"

        # Build the structured audit data frame record
        log_data = {
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "operational_status": [current_state],
            "temperature_c": [parameters.get("temperature", 0.0)],
            "ph": [parameters.get("ph", 0.0)],
            "agitation_rpm": [parameters.get("agitation_rpm", 0.0)],
            "aeration_lmin": [parameters.get("aeration_rate", 0.0)],
            "substrate_feed_kghr": [parameters.get("substrate_feed_rate", 0.0)],
            "t2_score": [round(evaluation_results.get("t2_value", 0.0), 3)],
            "spe_score": [round(evaluation_results.get("spe_value", 0.0), 3)]
        }
        
        df_new_log = pd.DataFrame(log_data)

        # Append row smoothly to the ongoing file system layer
        if not os.path.exists(log_file):
            df_new_log.to_csv(log_file, index=False)
        else:
            df_new_log.to_csv(log_file, mode='a', header=False, index=False)
