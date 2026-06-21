from typing import Protocol
from pydantic import BaseModel


class RetrievedDocument(BaseModel):
    title: str
    url: str
    excerpt: str


class Retriever(Protocol):
    async def search(self, query: str, limit: int = 5) -> list[RetrievedDocument]: ...


class LocalDocumentationRetriever:
    """Deterministic retriever used for tests and local demos.

    Production usage: replace this with pgvector, managed embeddings, and a
    freshness job that re-indexes official and internal documentation.
    """

    async def search(self, query: str, limit: int = 5) -> list[RetrievedDocument]:
        documents = [
            RetrievedDocument(
                title="FastAPI dependency injection",
                url="https://fastapi.tiangolo.com/tutorial/dependencies/",
                excerpt="Use dependencies to share validated resources across endpoints.",
            ),
            RetrievedDocument(
                title="PostgreSQL constraints",
                url="https://www.postgresql.org/docs/current/ddl-constraints.html",
                excerpt="Database constraints protect data integrity beyond application code.",
            ),
        ]
        return documents[:limit]
