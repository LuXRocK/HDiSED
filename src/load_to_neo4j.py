import json
import os
from neo4j import GraphDatabase
import glob

class Neo4jLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_data(self, data):
        with self.driver.session() as session:
            self._clear_db(session)
            self._create_nodes(session, data['elements'])
            self._create_relationships(session, data['relationships'])

    def _clear_db(self, session):
        print("Clearing the database...")
        session.run("MATCH (n) DETACH DELETE n")

    def _create_nodes(self, session, nodes):
        print("Creating nodes...")
        for node_data in nodes:
            query = f"CREATE (n:`{node_data['type']}` {{id: $id, description: $description}})"
            session.run(
                query,
                id=node_data['id'],
                description=node_data['description']
            )

    def _create_relationships(self, session, relationships):
        print("Creating relationships...")
        for rel_data in relationships:
            query = f"""
                MATCH (a {{id: $source}})
                MATCH (b {{id: $target}})
                CREATE (a)-[r:`{rel_data['label']}` {{context: $context}}]->(b)
                """
            session.run(
                query,
                source=rel_data['source'],
                target=rel_data['target'],
                context=rel_data['context']
            )

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load graph data from a specific model's output into Neo4j.")
    parser.add_argument("model_name", type=str, help="The name of the model directory to load data from (e.g., 'gemma', 'llama3').")
    args = parser.parse_args()

    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"
    
    loader = Neo4jLoader(uri, user, password)
    
    file_path = f"data/output/{args.model_name}/extracted_graph.json"
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        models = [d for d in os.listdir('data/output') if os.path.isdir(os.path.join('data/output', d))]
        print(f"Available models: {models}")
        exit(1)

    print(f"Processing file: {file_path}")
    with open(file_path, 'r') as f:
        data = json.load(f)
        loader.load_data(data)

    loader.close()
    print("Data loading complete.")