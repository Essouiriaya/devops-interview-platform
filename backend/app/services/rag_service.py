import logging

from app.core.config import settings
from app.services.knowledge_base import KNOWLEDGE_BASE

logger = logging.getLogger("uvicorn")


class RAGService:
    """Pipeline RAG : chunks -> embeddings SentenceTransformers -> Qdrant -> recherche sémantique."""

    def __init__(self):
        self._embedder = None
        self._qdrant = None
        self._vector_size = 384  # all-MiniLM-L6-v2

    def _init(self):
        if self._qdrant is not None:
            return
        from qdrant_client import QdrantClient
        from sentence_transformers import SentenceTransformer

        self._embedder = SentenceTransformer(settings.EMBEDDING_MODEL)
        try:
            self._qdrant = QdrantClient(url=settings.QDRANT_URL)
            self._qdrant.get_collections()  # vérifie la connexion
        except Exception:
            logger.warning("Qdrant serveur indisponible, utilisation du mode ':memory:'.")
            self._qdrant = QdrantClient(":memory:")

        from qdrant_client.models import Distance, VectorParams

        collections = [c.name for c in self._qdrant.get_collections().collections]
        if settings.QDRANT_COLLECTION not in collections:
            self._qdrant.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=VectorParams(size=self._vector_size, distance=Distance.COSINE),
            )
            self._index_documents()

    def _chunks(self) -> list[dict]:
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=60)
        docs = []
        for domain, texts in KNOWLEDGE_BASE.items():
            for t in texts:
                for i, chunk in enumerate(splitter.split_text(t)):
                    docs.append({"domain": domain, "text": chunk})
        return docs

    def _index_documents(self):
        from qdrant_client.models import PointStruct

        docs = self._chunks()
        embeddings = self._embedder.encode([d["text"] for d in docs]).tolist()
        points = [
            PointStruct(id=i, vector=emb, payload={"domain": d["domain"], "text": d["text"]})
            for i, (d, emb) in enumerate(zip(docs, embeddings))
        ]
        self._qdrant.upsert(collection_name=settings.QDRANT_COLLECTION, points=points)
        logger.info(f"{len(points)} chunks indexés dans Qdrant.")

    def retrieve(self, query: str, domain: str | None = None, k: int = 4) -> list[str]:
        """Retourne les k chunks les plus pertinents pour la requête."""
        try:
            self._init()
            vec = self._embedder.encode([query]).tolist()[0]
            filter_by = {"must": [{"key": "domain", "match": {"value": domain}}]} if domain else None
            results = self._qdrant.search(
                collection_name=settings.QDRANT_COLLECTION,
                query_vector=vec,
                query_filter=filter_by,
                limit=k,
            )
            return [r.payload["text"] for r in results]
        except Exception as e:
            logger.warning(f"RAG indisponible ({e}), contexte brut utilisé.")
            texts = KNOWLEDGE_BASE.get(domain) or [
                t for ts in KNOWLEDGE_BASE.values() for t in ts
            ]
            return texts[:k]


_rag = RAGService()


def get_rag_service() -> RAGService:
    return _rag