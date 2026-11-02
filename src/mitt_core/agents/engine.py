# Modification target inside src/mitt_core/agents/engine.py

def analyze_process_anomaly(self, snapshot: ProcessBatchSnapshot, statistical_metrics: dict, time_to_breach_min: float = None) -> str:
    graph_context = self.kg_connector.get_agent_formatted_context()
    system_prompt = BioprocessAgentPromptLibrary.get_core_diagnostic_system_prompt(graph_context)
    user_content = BioprocessAgentPromptLibrary.format_user_telemetry_payload(snapshot.dict(), statistical_metrics)

    # 👇 LINKED INJECTION: Update the payload using the prompt library method
    if time_to_breach_min is not None:
        user_content = BioprocessAgentPromptLibrary.append_predictive_instruction_block(
            base_user_content=user_content,
            time_to_breach_min=time_to_breach_min
        )

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
