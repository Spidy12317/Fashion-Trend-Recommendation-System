import numpy as np
import pickle
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NumPyVectorStore:
    def __init__(self):
        self.vectors = {}
        self.metadata = {}

    def create_index(self, index_name, dimension):
        if index_name in self.vectors:
            raise ValueError(f"Index '{index_name}' already exists")
        
        self.vectors[index_name] = []
        self.metadata[index_name] = []
        logger.info(f"Created index '{index_name}' with dimension {dimension}")

    def add_vector(self, index_name, vector, metadata=None):
        if index_name not in self.vectors:
            raise ValueError(f"Index '{index_name}' does not exist")
        
        vector = np.array(vector).astype('float32')
        self.vectors[index_name].append(vector)
        self.metadata[index_name].append(metadata)
        logger.info(f"Added vector to index '{index_name}'")

    def search(self, index_name, query_vector, k=5):
        if index_name not in self.vectors:
            raise ValueError(f"Index '{index_name}' does not exist")
        
        logger.info(f"Searching in index '{index_name}' for {k} nearest neighbors")
        
        query_vector = np.array(query_vector).astype('float32')
        vectors = np.array(self.vectors[index_name])
        
        if len(vectors) == 0:
            logger.warning(f"Index '{index_name}' is empty. No search performed.")
            return []

        distances = np.linalg.norm(vectors - query_vector, axis=1)
        nearest_indices = np.argsort(distances)[:k]
        
        results = []
        for idx in nearest_indices:
            results.append({
                'vector': self.vectors[index_name][idx].tolist(),
                'metadata': self.metadata[index_name][idx],
                'distance': float(distances[idx])
            })
        
        logger.info(f"Found {len(results)} results")
        return results

    def save(self, filepath):
        try:
            data = {
                'vectors': {k: [v.tolist() for v in vecs] for k, vecs in self.vectors.items()},
                'metadata': self.metadata
            }

            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info(f"Vector store saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise

    @classmethod
    def load(cls, filepath):
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)

            vector_store = cls()
            vector_store.vectors = {k: [np.array(v, dtype='float32') for v in vecs] for k, vecs in data['vectors'].items()}
            vector_store.metadata = data['metadata']

            logger.info(f"Vector store loaded from {filepath}")
            return vector_store
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise
