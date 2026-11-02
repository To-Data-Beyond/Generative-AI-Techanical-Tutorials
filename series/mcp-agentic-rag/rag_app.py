"""Original ten-question FAQ, native Nomic embeddings and durable local Qdrant."""
import hashlib
import re
import uuid
import threading
from pathlib import Path

import numpy as np
import torch
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient, models
from faq_data import PYTHON_FAQ_TEXT

MODEL_ID = "nomic-ai/nomic-embed-text-v1.5"
MODEL_REVISION = "e9b6763023c676ca8431644204f50c2b100d9aab"


def checked_query(query):
    if not isinstance(query, str) or not query.strip() or len(query) > 4096:
        raise ValueError("Expected a nonempty query of at most 4096 characters.")
    return query.strip()


def batch_generator(data, batch_size):
    if type(batch_size) is not int or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer.")
    for offset in range(0, len(data), batch_size):
        yield data[offset:offset + batch_size]


class FAQEngine:
    def __init__(self, storage_path, cache_folder=None):
        torch.set_num_threads(4)
        self.lock = threading.RLock()
        self.contexts = self.parse_faq(PYTHON_FAQ_TEXT)
        digest = hashlib.sha256(PYTHON_FAQ_TEXT.encode()).hexdigest()
        self.collection_name = "python_faq_" + digest[:12]
        self.source_hash = digest
        self.embed_model = HuggingFaceEmbedding(
            model_name=MODEL_ID, revision=MODEL_REVISION,
            trust_remote_code=False, token=False, device="cpu", max_length=512,
            query_instruction="search_query: ", text_instruction="search_document: ",
            normalize=True, cache_folder=cache_folder)
        self.vector_dim = len(self.embed_model.get_text_embedding("dimension probe"))
        self.client = QdrantClient(path=str(Path(storage_path).resolve()), force_disable_check_same_thread=True)

    @staticmethod
    def parse_faq(text):
        if not isinstance(text, str):
            raise TypeError("FAQ text must be a string, not an iterable of characters.")
        contexts = [part.strip() for part in re.split(r"\n(?=Question:)", text.strip()) if part.strip()]
        if not contexts or any(not p.startswith("Question:") or "\nAnswer:" not in p for p in contexts):
            raise ValueError("Each FAQ record needs a complete Question and Answer.")
        return contexts

    def setup_collection(self, batch_size=4):
        # Deterministic IDs and synchronous writes make repeated startup idempotent.
        list(batch_generator([], batch_size))
        if self.client.collection_exists(self.collection_name):
            config = self.client.get_collection(self.collection_name).config.params.vectors
            if config.size != self.vector_dim or config.distance != models.Distance.COSINE:
                raise ValueError("Existing collection has an incompatible vector configuration.")
            records, next_page = self.client.scroll(self.collection_name, limit=100, with_payload=True)
            expected = {str(uuid.uuid5(uuid.NAMESPACE_URL, value)) for value in self.contexts}
            if next_page or any(str(p.id) not in expected or p.payload.get("source_hash") != self.source_hash for p in records):
                raise ValueError("Refusing to overwrite a collection containing unrelated data.")
        else:
            self.client.create_collection(self.collection_name,
                vectors_config=models.VectorParams(size=self.vector_dim, distance=models.Distance.COSINE))
        for batch in batch_generator(list(enumerate(self.contexts, 1)), batch_size):
            vectors = self.embed_model.get_text_embedding_batch([value for _, value in batch])
            points = [models.PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL, context)),
                vector=vector, payload={"context": context, "source": f"FAQ:{index}", "source_hash": self.source_hash})
                for (index, context), vector in zip(batch, vectors, strict=True)]
            self.client.upsert(self.collection_name, points=points, wait=True)
        return self.client.count(self.collection_name, exact=True).count

    def answer_question(self, query, top_k=3):
        query = checked_query(query)
        if type(top_k) is not int or not 1 <= top_k <= 10:
            raise ValueError("top_k must be an integer from 1 to 10.")
        with self.lock:
            vector = self.embed_model.get_query_embedding(query)
            points = self.client.query_points(self.collection_name, query=vector, limit=top_k,
                score_threshold=0.5, with_payload=True).points
        return {"query": query, "contexts": [{"source": p.payload["source"],
            "context": p.payload["context"], "score": p.score} for p in points]}

    def close(self):
        self.client.close()
