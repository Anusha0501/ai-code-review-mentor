import asyncio
from backend.app.agents.graph import ReviewCoordinator
from backend.app.domain.models import DiffChunk, ExperienceLevel, PullRequestContext
from backend.app.rag.retriever import LocalDocumentationRetriever
from backend.app.repositories.reviews import ReviewRepository
from backend.app.services.review_service import ReviewService


def test_review_service_generates_mentoring_findings() -> None:
    async def run() -> None:
        service = ReviewService(
            repository=ReviewRepository(),
            coordinator=ReviewCoordinator(LocalDocumentationRetriever()),
        )
        context = PullRequestContext(
            repository="acme/web",
            pull_request_number=7,
            title="Add billing endpoint",
            author="dev",
            base_sha="abc",
            head_sha="def",
        )

        review = await service.review_diff(
            context=context,
            chunks=[DiffChunk(file_path="billing.py", patch="+ except Exception: pass")],
            developer_level=ExperienceLevel.beginner,
        )

        assert review.findings
        assert "underlying concept" in review.findings[0].explanation

    asyncio.run(run())
