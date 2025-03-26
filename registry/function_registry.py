from typing import List, Dict
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class FunctionRegistry:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
         
        self.model = SentenceTransformer(model_name)
         
        self.functions: Dict[str, Dict[str, List[str]]] = {
            "open_chrome": {
                "description": ["Open Chrome browser"],
                "keywords": ["chrome", "browser", "internet", "web"]
            },
            "open_calculator": {
                "description": ["Open system calculator"],
                "keywords": ["calculator", "compute", "math", "calculate"]
            },
            "get_system_resources": {
                "description": ["Check system performance"],
                "keywords": ["cpu", "memory", "resources", "performance"]
            },
            "run_shell_command": {
                "description": ["Execute shell command"],
                "keywords": ["command", "shell", "terminal", "execute"]
            }
        }
         
        self.embeddings = self._create_embeddings()
        self.index = self._create_faiss_index()

    def _create_embeddings(self) -> np.ndarray:
       
        texts = []
        for func in self.functions.values():
            # Combine descriptions and keywords
            combined_text = " ".join(
                func.get('description', []) + 
                func.get('keywords', [])
            )
            texts.append(combined_text)
        
        return self.model.encode(texts)

    def _create_faiss_index(self) -> faiss.IndexFlatL2:
         
        dimension = self.embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(self.embeddings)
        return index

    def search_functions(self, query: str, top_k: int = 1) -> List[str]:
        
        query_embedding = self.model.encode([query])
         
        distances, indices = self.index.search(query_embedding, top_k)
         
        matched_functions = [
            list(self.functions.keys())[idx] 
            for idx in indices[0]
        ]
        
        return matched_functions