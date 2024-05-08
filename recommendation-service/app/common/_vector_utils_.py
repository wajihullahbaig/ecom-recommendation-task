import numpy as np
from functools import lru_cache
from sentence_transformers import SentenceTransformer as EmbeddingTransformer

from common import ConfigVars

@lru_cache()
def get_model():
    return EmbeddingTransformer(ConfigVars.EMBEDDINGS_MODEL, device=ConfigVars.EMBEDDING_DEVICE)



def text_to_vector(text:str, perform_normalization:bool=False) -> np.ndarray:
    return get_model().encode(text, show_progress_bar=False, normalize_embeddings=perform_normalization)
