from functools import lru_cache
from backend.app.agents.graph import ReviewCoordinator
from backend.app.rag.retriever import LocalDocumentationRetriever
from backend.app.repositories.reviews import ReviewRepository
from backend.app.services.review_service import ReviewService


@lru_cache
def get_review_repository() -> ReviewRepository:
    return ReviewRepository()


def get_review_service() -> ReviewService:
    retriever = LocalDocumentationRetriever()
    coordinator = ReviewCoordinator(retriever=retriever)
    return ReviewService(repository=get_review_repository(), coordinator=coordinator)
