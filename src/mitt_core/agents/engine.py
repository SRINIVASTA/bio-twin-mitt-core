import os
import streamlit as st
from typing import Dict, Any, List
from groq import Groq
from src.mitt_core.domain.telemetry import ProcessBatchSnapshot


class GroqBioprocessAgentEngine:
    """
    Autonomous workflow manager utilizing Groq LLM architectures to process 
    real-time multi-variable fermentation anomalies and issue SOP-compliant recommendations.
    """
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        # Automatically fetches from .streamlit/secrets.toml or system environment variables
        self.api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY missing. Configure it in your environment or Streamlit secrets.")
        
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name

    def analyze_process_anomaly(
        self, 
        snapshot: ProcessBatchSnapshot, 
        statistical_metrics: Dict[str, Any]
    ) -> str:
        """
        Submits real-time soft-sensor telemetry metrics and statistical alarms 
        to Groq's low-latency inference endpoints for rapid diagnostic generation.
        """
        system_prompt = (
            "You are an expert Data Science and Automation Agent platform within a GxP "
            "validated pharmaceutical manufacturing environment. Your task is to analyze real-time "
            "bioprocess anomalies and provide strict, actionable decision-support summaries "
            "aligned with standard manufacturing SOPs."
        )

        user_content = f"""
        [CRITICAL PROCESS TELEMETRY ALERT]
        Batch ID: {snapshot.batch_id}
        Phase Duration: {snapshot.step_duration_hours} hours
        
        Current Sensor Values:
        {snapshot.parameters}
        
        Latent Variable Soft-Sensor Outputs:
        - Hotelling T² Score: {statistical_metrics['t2_value']:.4f} (Upper Limit: {statistical_metrics['t2_ucl']:.4f})
        - T² Breach Status: {statistical_metrics['t2_alarm']}
        - Squared Prediction Error (SPE): {statistical_metrics['spe_value']:.4f} (Upper Limit: {statistical_metrics['spe_ucl']:.4f})
        - SPE Breach Status: {statistical_metrics['spe_alarm']}
        
        INSTRUCTION: 
        Draft a high-priority summary detailing whether this anomaly constitutes a process shift (T² breach) 
        or an unmodeled raw material/mechanical fault (SPE breach). List exactly 3 immediate root-cause verification steps.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                model=self.model_name,
                temperature=0.1,  # Low temperature for deterministic, reliable GxP responses
                max_tokens=512
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error executing Groq LLM diagnostic pipeline: {str(e)}"
