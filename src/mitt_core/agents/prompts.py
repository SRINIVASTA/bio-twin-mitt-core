from typing import Dict, Any


class BioprocessAgentPromptLibrary:
    """
    Central repository for GxP-compliant system blueprints and operational 
    SOP prompts designed to govern autonomous bioprocess agent behavior.
    """
    
    @staticmethod
    def get_core_diagnostic_system_prompt(plant_taxonomy_context: str) -> str:
        """
        Generates a hardened system prompt that mandates strict adherence 
        to pharmaceutical standard operating guidelines and analytical boundaries.
        """
        return f"""
ROLE AND OBJECTIVE:
You are the lead Manufacturing Intelligence Decision-Support Agent for Pfizer's MITT platform. 
Your core objective is to analyze real-time multi-variable fermentation anomalies, diagnose potential 
root causes, and recommend precise, non-destructive Standard Operating Procedure (SOP) intervention paths.

ENVIRONMENT AND COMPLIANCE RULES:
- You operate within a strict GxP validated pharmaceutical manufacturing framework.
- You must prioritize batch safety, sterility, and containment above all output metrics.
- Your answers must be highly deterministic, analytical, concise, and free of speculative commentary.
- Never invent metrics, sensor values, or regulatory limits not explicitly present in the data packet.

PLANT TAXONOMY & REGULATORY SPECIFICATIONS:
{plant_taxonomy_context}

DIAGNOSTIC CRITERIA MATRIX (HOW TO INTERPRET SOFT SENSOR ALARMS):
1. Hotelling's T² Alarm Tripped = TRUE | SPE Anomaly Alarm Tripped = FALSE
   - DIAGNOSIS: Process Shift / Kinetic Drift. The system is still operating within known mathematical states, but has drifted away from the optimal Golden Batch envelope (e.g., pH/Temp setpoint drifting).
2. Hotelling's T² Alarm Tripped = ANY  | SPE Anomaly Alarm Tripped = TRUE
   - DIAGNOSIS: Unmodeled Disturbance / Mechanical Fault / Raw Material Deviation. A critical event has occurred that was not part of the historical training data (e.g., sensor failure, mechanical line breakage, feed contamination).

REQUIRED OUTPUT FORMAT STRUCTURE:
Your response must strictly utilize the following markdown structure, omitting any introductory conversational text:

### [BATCH ANOMALY REPORT]
- **Diagnostic Classification**: [Process Shift OR Unmodeled Disturbance]
- **Primary Breach Profile**: [Brief explanation of what T² or SPE statuses signify for this batch]

### [PROBABLE ROOT-CAUSE ANALYSIS]
- **Hypothesis 1**: [Description of highest probability failure mode based on sensor deviations]
- **Hypothesis 2**: [Description of secondary fallback failure scenario]

### [IMMEDIATE SOP CORRECTIVE VERIFICATION ACTIONS]
1. [Action 1: Mandatory localized hardware or sensor check fragment]
2. [Action 2: Quality parameter sampling or verification check fragment]
3. [Action 3: Contingency parameter restoration threshold step]
"""

    @staticmethod
    def format_user_telemetry_payload(snapshot_dict: Dict[str, Any], evaluation_results: Dict[str, Any]) -> str:
        """
        Convenience formatter to bundle telemetry parameters and statistical 
        anomaly metrics into a structured string block for user queries.
        """
        return f"""
[TELEMETRY METRIC REGISTRY]
- Batch ID: {snapshot_dict.get('batch_id')}
- Elapsed Cycle (Hours): {snapshot_dict.get('step_duration_hours')}
- Logged Parameter Array: {snapshot_dict.get('parameters')}

[SOFT-SENSOR LATENT VARIABLE FRAMEWORK METRICS]
- Hotelling T² Metric: {evaluation_results.get('t2_value', 0.0):.4f}
- Hotelling T² Upper Control Limit (UCL): {evaluation_results.get('t2_ucl', 0.0):.4f}
- Hotelling T² Limit Breach Status: {evaluation_results.get('t2_alarm')}

- Squared Prediction Error (SPE / Q): {evaluation_results.get('spe_value', 0.0):.4f}
- Squared Prediction Error (SPE) UCL: {evaluation_results.get('spe_ucl', 0.0):.4f}
- SPE Limit Breach Status: {evaluation_results.get('spe_alarm')}
"""


if __name__ == "__main__":
    print("Testing prompt library rendering output parameters...")
    sample_context = "BIOREACTOR_01 -> agitation_rpm [Bounds: 110-130 RPM]"
    sys_prompt = BioprocessAgentPromptLibrary.get_core_diagnostic_system_prompt(sample_context)
    
    assert "[BATCH ANOMALY REPORT]" in sys_prompt
    print("Prompt library integrity check: PASSED")
