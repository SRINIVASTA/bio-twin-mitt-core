from typing import Dict, List, Set, Optional
from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    """
    Represents an asset, parameter, or recipe specification boundary 
    within the pharmaceutical manufacturing taxonomy.
    """
    id: str = Field(..., description="Unique alphanumeric identifier for the node entity.")
    label: str = Field(..., description="The functional type/class of node (e.g., UNIT_OPERATION, CPP, CQA).")
    properties: Dict[str, str | float | List[float]] = Field(
        default_factory=dict, 
        description="Metadata attributes including target engineering units or GxP bounds."
    )


class GraphEdge(BaseModel):
    """
    Defines the directional relationship or regulatory dependency between two ontology nodes.
    """
    source: str = Field(..., description="The ID of the originating node entity.")
    target: str = Field(..., description="The ID of the destination node entity.")
    relationship: str = Field(..., description="The relationship type (e.g., MONITOR_TAG, CONTROLS, INFLUENCES).")


class BioprocessKnowledgeGraph:
    """
    An in-memory semantic knowledge graph designed to provide context to LLM 
    agents regarding critical bioprocess recipes, limits, and relationships.
    """
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.adjacency_list: Dict[str, List[GraphEdge]] = {}

    def add_node(self, node: GraphNode) -> None:
        """Adds a verified asset or parameter node to the bioprocess graph ontology."""
        self.nodes[node.id] = node
        if node.id not in self.adjacency_list:
            self.adjacency_list[node.id] = []

    def add_edge(self, edge: GraphEdge) -> None:
        """Establishes a semantic directional edge link between two existing nodes."""
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise KeyError(f"Both source '{edge.source}' and target '{edge.target}' must exist in the graph.")
        self.adjacency_list[edge.source].append(edge)

    def get_critical_process_parameters(self, unit_operation_id: str) -> List[GraphNode]:
        """
        Traverses the local adjacency matrix to extract all downstream Critical Process 
        Parameters (CPPs) assigned to a given unit operation.
        """
        cpp_nodes = []
        if unit_operation_id not in self.adjacency_list:
            return cpp_nodes

        for edge in self.adjacency_list[unit_operation_id]:
            if edge.relationship == "MONITOR_TAG":
                target_node = self.nodes.get(edge.target)
                if target_node and target_node.label == "CPP":
                    cpp_nodes.append(target_node)
        return cpp_nodes

    def export_agent_context(self) -> Dict[str, Any]:
        """
        Serializes the active topological relations into a compressed structured text map 
        suitable for feeding directly into LLM system prompt context windows.
        """
        context = {"entities": [], "dependencies": []}
        for node in self.nodes.values():
            context["entities"].append({
                "id": node.id,
                "type": node.label,
                "specs": node.properties
            })
        for edges in self.adjacency_list.values():
            for edge in edges:
                context["dependencies"].append(
                    f"{edge.source} --[{edge.relationship}]--> {edge.target}"
                )
        return context


if __name__ == "__main__":
    # Test layout mapping to verify proper graph topology construction
    print("Initializing structural Bioprocess Knowledge Graph framework...")
    kg = BioprocessKnowledgeGraph()
    
    # Define corporate asset entities
    kg.add_node(GraphNode(id="R-101", label="UNIT_OPERATION", properties={"desc": "Primary Fermentation Bioreactor"}))
    kg.add_node(GraphNode(id="agitation_rpm", label="CPP", properties={"min_limit": 100.0, "max_limit": 140.0, "unit": "RPM"}))
    kg.add_node(GraphNode(id="penicillin_v_titer", label="CQA", properties={"target_min": 15.2, "unit": "g/L"}))
    
    # Establish semantic directional relationships
    kg.add_edge(GraphEdge(source="R-101", target="agitation_rpm", relationship="MONITOR_TAG"))
    kg.add_edge(GraphEdge(source="agitation_rpm", target="penicillin_v_titer", relationship="INFLUENCES"))
    
    cpps = kg.get_critical_process_parameters("R-101")
    print(f"Graph initialized successfully. Extracted CPP count for R-101: {len(cpps)}")
    print(f"Sample Node Constraint Mapping: {cpps[0].properties}")
