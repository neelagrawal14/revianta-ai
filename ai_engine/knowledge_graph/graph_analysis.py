from typing import Dict, List, Any


class KnowledgeGraphAnalyzer:
    """
    Analyzes the knowledge graph created by KnowledgeGraphBuilder.

    Stage 1:
    - Rule-based graph analysis
    - No database dependency
    - No graph database dependency
    """

    def __init__(self, graph: Dict[str, Any]):
        self.graph = graph
        self.nodes = graph.get("nodes", [])
        self.edges = graph.get("edges", [])

    def get_nodes_by_type(self, node_type: str) -> List[Dict[str, Any]]:
        """
        Return all nodes belonging to a specific type.
        """

        return [
            node
            for node in self.nodes
            if node.get("type") == node_type
        ]

    def get_project_node(self) -> Dict[str, Any]:
        """
        Return the project node.
        """

        projects = self.get_nodes_by_type("Project")

        if not projects:
            return {}

        return projects[0]

    def get_connected_nodes(
        self,
        node_id: str
    ) -> List[Dict[str, Any]]:
        """
        Return nodes directly connected to a given node.
        """

        connected_ids = set()

        for edge in self.edges:

            if edge["source"] == node_id:
                connected_ids.add(edge["target"])

            elif edge["target"] == node_id:
                connected_ids.add(edge["source"])

        return [
            node
            for node in self.nodes
            if node["id"] in connected_ids
        ]

    def get_project_relationships(self) -> List[Dict[str, Any]]:
        """
        Return all relationships originating from the project.
        """

        project = self.get_project_node()

        if not project:
            return []

        return [
            edge
            for edge in self.edges
            if edge["source"] == project["id"]
        ]

    def calculate_node_degrees(self) -> Dict[str, int]:
        """
        Calculate how many relationships each node has.
        """

        degrees = {
            node["id"]: 0
            for node in self.nodes
        }

        for edge in self.edges:

            source = edge["source"]
            target = edge["target"]

            if source in degrees:
                degrees[source] += 1

            if target in degrees:
                degrees[target] += 1

        return degrees

    def get_most_connected_nodes(
        self,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Return the most connected nodes.
        """

        degrees = self.calculate_node_degrees()

        ranked = sorted(
            degrees.items(),
            key=lambda item: item[1],
            reverse=True
        )

        results = []

        for node_id, degree in ranked[:top_k]:

            node = next(
                (
                    node
                    for node in self.nodes
                    if node["id"] == node_id
                ),
                None
            )

            if node:

                results.append({
                    "node": node,
                    "degree": degree
                })

        return results

    def get_graph_summary(self) -> Dict[str, Any]:
        """
        Generate a high-level summary of the knowledge graph.
        """

        type_counts = {}

        for node in self.nodes:

            node_type = node["type"]

            type_counts[node_type] = (
                type_counts.get(node_type, 0) + 1
            )

        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": type_counts
        }

    def analyze(self) -> Dict[str, Any]:
        """
        Run complete graph analysis.
        """

        project = self.get_project_node()

        relationships = self.get_project_relationships()

        connected_nodes = []

        if project:
            connected_nodes = self.get_connected_nodes(
                project["id"]
            )

        return {
            "summary": self.get_graph_summary(),
            "project": project,
            "project_relationships": relationships,
            "connected_nodes": connected_nodes,
            "most_connected_nodes": self.get_most_connected_nodes()
        }


if __name__ == "__main__":

    from .graph_builder import KnowledgeGraphBuilder

    builder = KnowledgeGraphBuilder()

    graph = builder.build_project_graph(

        project_name="AI-Powered Satellite Image Analysis",

        technologies=[
            "Satellite Image Analysis",
            "Computer Vision",
            "Geospatial Data",
            "Deep Learning",
            "Optical Imagery",
            "SAR",
            "Artificial Intelligence"
        ],

        keywords=[
            "urban development",
            "satellite imagery",
            "infrastructure",
            "building",
            "road"
        ],

        related_papers=[
            {
                "title": "Deep Learning for Satellite Image Analysis",
                "similarity": 0.7629
            },
            {
                "title": "Urban Development Detection Using Remote Sensing",
                "similarity": 0.65
            }
        ],

        datasets=[
            {
                "name": "Satellite Urban Dataset",
                "source": "Example Dataset"
            }
        ],

        patents=[
            {
                "title": "Satellite Image Processing System"
            }
        ]
    )

    analyzer = KnowledgeGraphAnalyzer(graph)

    result = analyzer.analyze()

    print("\n========== KNOWLEDGE GRAPH ANALYSIS ==========\n")

    print("GRAPH SUMMARY")

    print(
        f"Total Nodes: "
        f"{result['summary']['total_nodes']}"
    )

    print(
        f"Total Edges: "
        f"{result['summary']['total_edges']}"
    )

    print("\nNODE TYPES")

    for node_type, count in result["summary"]["node_types"].items():
        print(f"- {node_type}: {count}")

    print("\nPROJECT CONNECTIONS")

    for node in result["connected_nodes"]:
        print(
            f"- [{node['type']}] "
            f"{node['name']}"
        )

    print("\nMOST CONNECTED NODES")

    for item in result["most_connected_nodes"]:

        print(
            f"- {item['node']['name']} "
            f"({item['node']['type']}) "
            f"→ {item['degree']} connections"
        )