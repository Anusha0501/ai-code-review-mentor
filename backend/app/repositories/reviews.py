from backend.app.domain.models import Review


class ReviewRepository:
    """In-memory repository for local development.

    Production usage: implement the same methods with SQLAlchemy or SQLModel
    backed by PostgreSQL and pgvector for review analytics.
    """

    def __init__(self) -> None:
        self._reviews: dict[str, Review] = {}

    async def save(self, review: Review) -> Review:
        self._reviews[review.id] = review
        return review

    async def list(self) -> list[Review]:
        return list(self._reviews.values())

    async def get(self, review_id: str) -> Review | None:
        return self._reviews.get(review_id)
