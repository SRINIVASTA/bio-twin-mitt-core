from src.mitt_core.domain.knowledge_graph import BioprocessKnowledgeGraph, GraphNode, GraphEdge


class KnowledgeGraphAgentConnector:
    def __init__(self):
        self.kg = BioprocessKnowledgeGraph()
        self._bootstrap_local_nodes()

    def _bootstrap_local_nodes(self) -> None:
        self.kg.add_node(GraphNode(id="BIOREACTOR_R101", label="EQUIPMENT", properties={"vessel_type": "Stainless Steel Production Vessel"}))
        self.kg.add_node(GraphNode(id="agitation_rpm", label="CPP", properties={"lower_limit": 110.0, "upper_limit": 130.0}))
        self.kg.add_node(GraphNode(id="temperature", label="CPP", properties={"lower_limit": 24.5, "upper_limit": 25.5}))
        self.kg.add_edge(GraphEdge(source="BIOREACTOR_R101", target="agitation_rpm", relationship="MONITOR_TAG"))
        self.kg.add_edge(GraphEdge(source="BIOREACTOR_R101", target="temperature", relationship="MONITOR_TAG"))

    def get_agent_formatted_context(self) -> str:
        raw_map = self.kg.export_agent_context()
        lines = ["Active Plant Network Mappings:"]
        for entity in raw_map["entities"]:
            lines.append(f" - Element ID: {entity['id']} ({entity['type']}) | Specs: {entity['specs']}")
        for dep in raw_map["dependencies"]:
            lines.append(f" - Relationship Dependency Path: {dep}")
        return "\n".join(lines)
