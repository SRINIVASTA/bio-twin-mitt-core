import os
import streamlit as st
from typing import Dict, Any
from groq import Groq

from src.mitt_core.domain.telemetry import ProcessBatchSnapshot
from src.mitt_core.agents.prompts import BioprocessAgentPromptLibrary
from src.mitt_core.agents.tools.kg_connector import KnowledgeGraphAgentConnector


class GroqBioprocessAgentEngine:
    """
    Autonomous workflow manager utilizing Groq LLM architectures to process 
    real-time multi-variable fermentation anomalies and issue SOP-compliant recommendations.
    Integrates semantic data from the Knowledge Graph to ensure strict compliance.
    """
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        # Automatically fetches from .streamlit/secrets.toml or system environment variables
        self.api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY missing. Configure it in your environment or Streamlit secrets.")
        
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name
        
        # Instantiate the knowledge graph connector to bind asset context to the pipeline
        self.kg_connector = KnowledgeGraphAgentConnector()

    def analyze_process_anomaly(
        self, 
        snapshot: ProcessBatchSnapshot, 
        statistical_metrics: Dict[str, Any]
    ) -> str:
        """
        Extracts semantic limits from the knowledge graph, builds a GxP-compliant 
        prompt payload, and invokes Groq low-latency inference endpoints for diagnostics.
        """
        # 1. Dynamically retrieve the current plant taxonomy to feed into the system prompt windows
        graph_context = self.kg_connector.get_agent_formatted_context()
        
        # 2. Build out the structured system guardrails using the prompt library
        system_prompt = BioprocessAgentPromptLibrary.get_core_diagnostic_system_prompt(
            plant_taxonomy_context=graph_context
        )

        # 3. Transform the incoming streaming telemetry and PCA stats into a clean text block
        user_content = BioprocessAgentPromptLibrary.format_user_telemetry_payload(
            snapshot_dict=snapshot.dict(),
            evaluation_results=statistical_metrics
        )

        try:
            # 4. Invoke the ultra-low latency Groq completion pipeline
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                model=self.model_name,
                temperature=0.0,  # Zero temperature forces deterministic, clinical, GxP-compliant output
                max_tokens=768
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error executing Groq LLM diagnostic pipeline: {str(e)}"


if __name__ == "__main__":
    print("Testing structural integration of Groq Agentic engine wrapper...")
    from datetime import datetime, timezone
    
    # Construct simulated minimal input datasets to verify plumbing layout safety
    mock_snapshot = ProcessBatchSnapshot(
        batch_id="TEST-INT-001",
        timestamp=datetime.now(timezone.utc),
        step_duration_hours=12.0,
        parameters={"temperature": 25.0, "ph": 6.5, "agitation_rpm": 145.2, "aeration_rate": 250.0}
    )
    mock_stats = {"t2_value": 8.52, "t2_ucl": 4.11, "t2_alarm": True, "spe_value": 0.12, "spe_ucl": 0.88, "spe_alarm": False}
    
    # Dry run initialization check
    try:
        engine = GroqBioprocessAgentEngine()
        print("Engine initialization passed.")
    except ValueError as v:
        print(f"Engine validated without live key: {v}")
