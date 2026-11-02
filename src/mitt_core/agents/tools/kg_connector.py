from typing import Dict, Any, Optional
from src.mitt_core.domain.knowledge_graph import BioprocessKnowledgeGraph, GraphNode, GraphEdge


class KnowledgeGraphAgentConnector:
    """
    Acts as an execution tool interface allowing Agentic AI frameworks to query 
    underlying semantic assets, recipe structures, and regulatory parameters.
    """
    def __init__(self, knowledge_graph: Optional[BioprocessKnowledgeGraph] = None):
        # Fallback to populating an internal default standard configuration map if none is provided
        if knowledge_graph is None:
            self.kg = BioprocessKnowledgeGraph()
            self._bootstrap_default_ontology()
        else:
            self.kg = knowledge_graph

    def _bootstrap_default_ontology(self) -> None:
        """Populates baseline seed records mirroring the IndPenSim process context."""
        # Add primary unit operations
        self.kg.add_node(GraphNode(id="BIOREACTOR_01", label="UNIT_OPERATION", properties={"vessel_volume_liters": 100000.0}))
        
        # Add Critical Process Parameters (CPPs)
        self.kg.add_node(GraphNode(id="temperature", label="CPP", properties={"lower_bound": 24.0, "upper_bound": 26.0, "unit": "degC"}))
        self.kg.add_node(GraphNode(id="ph", label="CPP", properties={"lower_bound": 6.30, "upper_bound": 6.70, "unit": "pH_units"}))
        self.kg.add_node(GraphNode(id="agitation_rpm", label="CPP", properties={"lower_bound": 110.0, "upper_bound": 130.0, "unit": "RPM"}))
        self.kg.add_node(GraphNode(id="aeration_rate", label="CPP", properties={"lower_bound": 240.0, "upper_bound": 260.0, "unit": "L/min"}))
        
        # Formulate structural edge attachments
        for param in ["temperature", "ph", "agitation_rpm", "aeration_rate"]:
            self.kg.add_edge(GraphEdge(source="BIOREACTOR_01", target=param, relationship="MONITOR_TAG"))

    def query_parameter_bounds(self, parameter_id: str) -> Dict[str, Any]:
        """
        Tool callable by the LLM agent loop to safely verify exact regulatory 
        manufacturing limit values for a specific process variable.
        """
        node = self.kg.nodes.get(parameter_id)
        if not node:
            return {"error": f"Parameter '{parameter_id}' was not located inside the active plant ontology."}
            
        return {
            "parameter": parameter_id,
            "class": node.label,
            "limits": node.properties
        }

    def get_agent_formatted_context(self) -> str:
        """
        Transforms the active manufacturing graph layout into a clean, text-based
        summary that can be easily fed directly into system prompts.
        """
        raw_map = self.kg.export_agent_context()
        
        output_lines = ["[KNOWLEDGE GRAPH PLANT TAXONOMY]"]
        output_lines.append("\nRegistered Manufacturing Entities:")
        for entity in raw_map["entities"]:
            output_lines.append(f" - Asset ID: {entity['id']} | Category: {entity['type']} | Specifications: {entity['specs']}")
            
        output_lines.append("\nActive Process Dependencies:")
        for dependency in raw_map["dependencies"]:
            output_lines.append(f" - {dependency}")
            
        return "\n".join(output_lines)


if __name__ == "__main__":
    # Validate execution standalone tool performance outputs
    print("Executing integration check on Agent Knowledge Graph interface adapter...")
    connector = KnowledgeGraphAgentConnector()
    print(connector.get_agent_formatted_context())
    
    print("\nExecuting sample live lookup on parameter bounds:")
    print(connector.query_parameter_bounds("agitation_rpm"))
