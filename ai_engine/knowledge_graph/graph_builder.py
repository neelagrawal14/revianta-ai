from typing import Dict, List, Any


class KnowledgeGraphBuilder:
    """
    Builds a lightweight research knowledge graph for Revianta AI.

    Stage 1:
    - No database dependency
    - No Neo4j dependency
    - Uses Python dictionaries
    - Creates explainable nodes and relationships

    Future versions can persist this graph in PostgreSQL/pgvector
    or a dedicated graph database.
    """

    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(
        self,
        node_id: str,
        node_type: str,
        name: str,
        properties: Dict[str, Any] = None
    ):
        """
        Add a node to the knowledge graph.
        """

        node = {
            "id": node_id,
            "type": node_type,
            "name": name,
            "properties": properties or {}
        }

        # Avoid duplicate nodes
        if not any(existing["id"] == node_id for existing in self.nodes):
            self.nodes.append(node)

    def add_edge(
        self,
        source: str,
        relation: str,
        target: str,
        properties: Dict[str, Any] = None
    ):
        """
        Add a relationship between two nodes.
        """

        edge = {
            "source": source,
            "relation": relation,
            "target": target,
            "properties": properties or {}
        }

        self.edges.append(edge)

    def build_project_graph(
        self,
        project_name: str,
        technologies: List[str],
        keywords: List[str],
        related_papers: List[Dict[str, Any]] = None,
        datasets: List[Dict[str, Any]] = None,
        patents: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build a knowledge graph around a research project.
        """

        # Reset graph
        self.nodes = []
        self.edges = []

        # --------------------------------------------------
        # PROJECT NODE
        # --------------------------------------------------

        project_id = "project_1"

        self.add_node(
            node_id=project_id,
            node_type="Project",
            name=project_name
        )

        # --------------------------------------------------
        # TECHNOLOGY NODES
        # --------------------------------------------------

        for index, technology in enumerate(technologies):

            technology_id = f"technology_{index + 1}"

            self.add_node(
                node_id=technology_id,
                node_type="Technology",
                name=technology
            )

            self.add_edge(
                source=project_id,
                relation="USES",
                target=technology_id
            )

        # --------------------------------------------------
        # KEYWORD NODES
        # --------------------------------------------------

        for index, keyword in enumerate(keywords):

            keyword_id = f"keyword_{index + 1}"

            self.add_node(
                node_id=keyword_id,
                node_type="Keyword",
                name=keyword
            )

            self.add_edge(
                source=project_id,
                relation="HAS_KEYWORD",
                target=keyword_id
            )

        # --------------------------------------------------
        # PAPER NODES
        # --------------------------------------------------

        if related_papers:

            for index, paper in enumerate(related_papers):

                paper_id = f"paper_{index + 1}"

                paper_name = paper.get(
                    "title",
                    f"Research Paper {index + 1}"
                )

                self.add_node(
                    node_id=paper_id,
                    node_type="Paper",
                    name=paper_name,
                    properties=paper
                )

                similarity = paper.get("similarity")

                self.add_edge(
                    source=project_id,
                    relation="SIMILAR_TO",
                    target=paper_id,
                    properties={
                        "similarity": similarity
                    }
                )

        # --------------------------------------------------
        # DATASET NODES
        # --------------------------------------------------

        if datasets:

            for index, dataset in enumerate(datasets):

                dataset_id = f"dataset_{index + 1}"

                dataset_name = dataset.get(
                    "name",
                    f"Dataset {index + 1}"
                )

                self.add_node(
                    node_id=dataset_id,
                    node_type="Dataset",
                    name=dataset_name,
                    properties=dataset
                )

                self.add_edge(
                    source=project_id,
                    relation="USES_DATASET",
                    target=dataset_id
                )

        # --------------------------------------------------
        # PATENT NODES
        # --------------------------------------------------

        if patents:

            for index, patent in enumerate(patents):

                patent_id = f"patent_{index + 1}"

                patent_name = patent.get(
                    "title",
                    f"Patent {index + 1}"
                )

                self.add_node(
                    node_id=patent_id,
                    node_type="Patent",
                    name=patent_name,
                    properties=patent
                )

                self.add_edge(
                    source=project_id,
                    relation="RELATED_TO",
                    target=patent_id
                )

        return self.get_graph()

    def get_graph(self) -> Dict[str, Any]:
        """
        Return the complete knowledge graph.
        """

        return {
            "nodes": self.nodes,
            "edges": self.edges,
            "node_count": len(self.nodes),
            "edge_count": len(self.edges)
        }


if __name__ == "__main__":

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

    print("\n========== KNOWLEDGE GRAPH ==========\n")

    print("Nodes:")

    for node in graph["nodes"]:
        print(
            f"- [{node['type']}] "
            f"{node['name']}"
        )

    print("\nRelationships:")

    for edge in graph["edges"]:
        print(
            f"- {edge['source']} "
            f"--{edge['relation']}--> "
            f"{edge['target']}"
        )

    print("\nGraph Statistics:")
    print(f"Nodes: {graph['node_count']}")
    print(f"Edges: {graph['edge_count']}")