from uuid import uuid4
from backend.app.agents.graph import ReviewCoordinator, ReviewGraphState
from backend.app.domain.models import DiffChunk, ExperienceLevel, PullRequestContext, Review
from backend.app.repositories.reviews import ReviewRepository


class ReviewService:
    def __init__(self, repository: ReviewRepository, coordinator: ReviewCoordinator) -> None:
        self.repository = repository
        self.coordinator = coordinator

    async def review_diff(
        self,
        context: PullRequestContext,
        chunks: list[DiffChunk],
        developer_level: ExperienceLevel,
    ) -> Review:
        state = await self.coordinator.run(
            ReviewGraphState(chunks=chunks, developer_level=developer_level)
        )
        review = Review(
            id=str(uuid4()),
            context=context,
            findings=state.findings,
            summary=state.summary,
        )
        return await self.repository.save(review)
