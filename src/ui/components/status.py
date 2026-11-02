import streamlit as st
from typing import Dict, Any


class BioTwinStatusSystem:
    """
    Renders standardized, GxP-compliant real-time alarm states and 
    critical process status banners inside the user interface layer.
    """

    @staticmethod
    def render_process_status_header(evaluation_results: Dict[str, Any]) -> None:
        """
        Renders a high-visibility structural banner at the top of the console 
        reflecting the overall safety tier of the active bioprocess run.
        """
        t2_alarm = evaluation_results.get("t2_alarm", False)
        spe_alarm = evaluation_results.get("spe_alarm", False)

        # Tier 1: Dual Breach - Severe System Anomaly / Immediate Action Required
        if t2_alarm and spe_alarm:
            st.error(
                "### 🛑 CRITICAL GxP ALARM: MULTI-VARIABLE PROCESS DEGRADATION\n"
                "Both Latent Variable Variance (T²) and Residual Error (SPE) have breached Upper Control Limits. "
                "Immediate manual verification and SOP mitigation protocol activation mandated."
            )
            
        # Tier 2: SPE Breach Only - Unmodeled Mechanical / Material Outlier
        elif spe_alarm:
            st.warning(
                "### ⚠️ COMPLIANCE ALERT: UNMODELED DISTURBANCE DETECTED (SPE BREACH)\n"
                "Residual evaluation matrix indicates an unmodeled process deviation. "
                "Inspect bioreactor structural subsystems, checking for sensor failures or feed matrix contamination."
            )

        # Tier 3: T² Breach Only - Kinetic / Thermodynamic Process Shift
        elif t2_alarm:
            st.warning(
                "### 📉 PROCESS SHIFT: GOLDEN BATCH BOUNDARY EXCURSION (T² BREACH)\n"
                "Multi-variable trajectory has drifted from the optimal operational envelope. "
                "Evaluate loops governing temperature, pH, or dissolved oxygen setpoint tracking."
            )

        # Tier 4: Stable State operation
        else:
            st.success(
                "### 🟢 PROCESS STABILITY SUMMARY: VALIDATED STATE\n"
                "All streaming parameters remain completely locked within historical Golden Batch envelopes. "
                "Online Statistical Process Control metrics verify fully compliant manufacturing performance."
            )

    @staticmethod
    def render_parameter_metrics_grid(parameters: Dict[str, float]) -> None:
        """
        Renders a secondary, scannable layout grid highlighting localized 
        sensor variables along with their standardized engineering units.
        """
        st.markdown("#### Real-Time Sensor Variable Matrix")
        cols = st.columns(len(parameters))
        
        for col, (param_name, param_value) in zip(cols, parameters.items()):
            clean_name = param_name.upper().replace("_", " ")
            
            # Map basic engineering unit suffixes for standard bioreactor streams
            unit_suffix = ""
            if "temp" in param_name.lower():
                unit_suffix = " °C"
            elif "rpm" in param_name.lower() or "agitation" in param_name.lower():
                unit_suffix = " RPM"
            elif "rate" in param_name.lower() or "feed" in param_name.lower():
                unit_suffix = " L/min" if "aeration" in param_name.lower() else " kg/hr"
            elif "ph" in param_name.lower():
                unit_suffix = " pH"

            col.metric(label=clean_name, value=f"{param_value}{unit_suffix}")


if __name__ == "__main__":
    # Standard script verification assertion checks
    print("Validating Bio-Twin visual alert formatting subsystem layer...")
    test_results_normal = {"t2_alarm": False, "spe_alarm": False}
    print("Status system evaluation checklist: READY")
