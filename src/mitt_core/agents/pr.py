from typing import Dict, Any


class BioprocessAgentPromptLibrary:
    @staticmethod
    def get_core_diagnostic_system_prompt(plant_taxonomy_context: str) -> str:
        return f"""ROLE: Lead Digital Twin Decision Support Agent for Pfizer MITT platform.
COMPLIANCE: Enforce strict Pharma 4.0 GxP compliance. Output must be concise and deterministic.

PLANT TAXONOMY CONTEXT:
{plant_taxonomy_context}

DIAGNOSTIC FAULT LOGIC MATRIX:
- T² Alarm = TRUE, SPE Alarm = FALSE -> Process Shift / Trajectory drift within modeled domain.
- SPE Alarm = TRUE -> Unmodeled mechanical disturbance / Raw material exception profile.

OUTPUT MANDATE: Return clear markdown tracking text matching the layout blocks below. 
Do not include any pleasantries or introductory conversational text.

### [BATCH ANOMALY REPORT]
- **Diagnostic Classification**: [Process Shift OR Unmodeled Disturbance]
- **Primary Breach Profile**: [Brief status sentence]

### [PROBABLE ROOT-CAUSE ANALYSIS]
- **Hypothesis 1**: [Failure explanation detail]

### [IMMEDIATE SOP CORRECTIVE VERIFICATION ACTIONS]
1. [Step 1 manual inspection validation instruction]
2. [Step 2 control loop inspection checklist parameter]
"""

    @staticmethod
    def format_user_telemetry_payload(snapshot_dict: Dict[str, Any], evaluation_results: Dict[str, Any]) -> str:
        return f"""[LIVE PROCESS VECTOR]
Parameters: {snapshot_dict.get('parameters')}
[MULTIVARIATE SOFT SENSOR CALCULATION ARRAYS]
- Hotelling T²: {evaluation_results.get('t2_value'):.4f} (Limit UCL: {evaluation_results.get('t2_ucl'):.4f}) | Breach: {evaluation_results.get('t2_alarm')}
- SPE Residual: {evaluation_results.get('spe_value'):.4f} (Limit UCL: {evaluation_results.get('spe_ucl'):.4f}) | Breach: {evaluation_results.get('spe_alarm')}
"""
