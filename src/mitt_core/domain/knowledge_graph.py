from typing import Dict, List, Any
from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    id: str = Field(..., description="Unique identification name.")
    label: str = Field(..., description="Asset type categorization tag.")
    properties: Dict[str, Any] = Field(default_factory=dict, description="GxP metadata limit boundaries.")


class GraphEdge(BaseModel):
    source: str = Field(..., description="Origin node.")
    target: str = Field(..., description="Destination node.")
    relationship: str = Field(..., description="Semantic connection logic.")


class BioprocessKnowledgeGraph:
    """In-memory semantic data layers defining operational asset envelopes."""
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.adjacency_list: Dict[str, List[GraphEdge]] = {}

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.id] = node
        if node.id not in self.adjacency_list:
            self.adjacency_list[node.id] = []

    def add_edge(self, edge: GraphEdge) -> None:
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise KeyError(f"Nodes '{edge.source}' or '{edge.target}' missing inside graph dictionary structures.")
        self.adjacency_list[edge.source].append(edge)

    def export_agent_context(self) -> Dict[str, Any]:
        context = {"entities": [], "dependencies": []}
        for node in self.nodes.values():
            context["entities"].append({"id": node.id, "type": node.label, "specs": node.properties})
        for edges in self.adjacency_list.values():
            for edge in edges:
                context["dependencies"].append(f"{edge.source} --[{edge.relationship}]--> {edge.target}")
        return context
