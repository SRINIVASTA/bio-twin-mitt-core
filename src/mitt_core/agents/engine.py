import os
import streamlit as st
from groq import Groq
from src.mitt_core.domain.telemetry import ProcessBatchSnapshot
from src.mitt_core.agents.prompts import BioprocessAgentPromptLibrary
from src.mitt_core.agents.tools.kg_connector import KnowledgeGraphAgentConnector
from config.base import GROQ_MODEL_TARGET


class GroqBioprocessAgentEngine:
    """Manages low-latency validation completion diagnostics using official Groq client wrappers."""
    def __init__(self):
        self.api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Authentication credentials for GROQ_API_KEY are missing from environment.")
        self.client = Groq(api_key=self.api_key)
        self.kg_connector = KnowledgeGraphAgentConnector()

    def analyze_process_anomaly(self, snapshot: ProcessBatchSnapshot, statistical_metrics: dict, time_to_breach_min: float = None) -> str:
        graph_context = self.kg_connector.get_agent_formatted_context()
        system_prompt = BioprocessAgentPromptLibrary.get_core_diagnostic_system_prompt(graph_context)
        user_content = BioprocessAgentPromptLibrary.format_user_telemetry_payload(snapshot.dict(), statistical_metrics)

        # 👇 PREDICTIVE EXTRACTION INTEGRATION LAYER
        # If a lookahead breach is actively identified, append a preventive structural instruction override
        if time_to_breach_min is not None:
            predictive_instruction_override = (
                f"\n\n⚠️ [🔮 ENTERPRISE PREDICTIVE ALERT OVERRIDE] ⚠️\n"
                f"CRITICAL COMPLIANCE NOTICE: A linear slope trend analysis projects that a hard boundary "
                f"Red Alert violation will occur in exactly {time_to_breach_min:.2f} MINUTES if operations continue unmodified.\n"
                f"Your primary objective is to pivot output generation from a reactive failure report to a "
                f"PROACTIVE PREVENTIVE STABILIZATION PLAN. Detail immediate regulatory-compliant adjustment targets to keep the batch safe."
            )
            user_content += predictive_instruction_override

        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                model=GROQ_MODEL_TARGET,
                temperature=0.0,
                max_tokens=512
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Failed to execute diagnostic loop sequence via Groq network engine channels: {str(e)}"
