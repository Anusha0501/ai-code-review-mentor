from fastapi import Depends, FastAPI, HTTPException, Request
from backend.app.api.dependencies import get_review_repository, get_review_service
from backend.app.domain.models import DiffChunk, ExperienceLevel, PullRequestContext, Review
from backend.app.repositories.reviews import ReviewRepository
from backend.app.services.review_service import ReviewService

app = FastAPI(title="ai-code-review-mentor", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhooks/github")
async def github_webhook(request: Request) -> dict[str, str]:
    # Production note: validate X-Hub-Signature-256 before trusting payloads.
    payload = await request.json()
    return {"status": "accepted", "event": payload.get("action", "unknown")}


@app.get("/reviews", response_model=list[Review])
async def list_reviews(repository: ReviewRepository = Depends(get_review_repository)) -> list[Review]:
    return await repository.list()


@app.get("/reviews/{review_id}", response_model=Review)
async def get_review(review_id: str, repository: ReviewRepository = Depends(get_review_repository)) -> Review:
    review = await repository.get(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@app.get("/analytics/summary")
async def analytics_summary(repository: ReviewRepository = Depends(get_review_repository)) -> dict[str, int]:
    reviews = await repository.list()
    findings = sum(len(review.findings) for review in reviews)
    return {"reviews": len(reviews), "findings": findings}


@app.post("/playground/review", response_model=Review)
async def playground_review(service: ReviewService = Depends(get_review_service)) -> Review:
    context = PullRequestContext(
        repository="demo/api",
        pull_request_number=42,
        title="Improve webhook handling",
        author="mentor-user",
        base_sha="base",
        head_sha="head",
        developer_level=ExperienceLevel.intermediate,
    )
    chunks = [DiffChunk(file_path="app/webhook.py", patch="+ # TODO validate signature")]
    return await service.review_diff(context, chunks, ExperienceLevel.intermediate)
