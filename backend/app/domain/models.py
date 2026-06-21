from datetime import datetime, timezone
from enum import StrEnum
from pydantic import BaseModel, Field


class ExperienceLevel(StrEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    senior = "senior"


class Severity(StrEnum):
    info = "info"
    warning = "warning"
    critical = "critical"


class PullRequestContext(BaseModel):
    repository: str
    pull_request_number: int
    title: str
    author: str
    base_sha: str
    head_sha: str
    developer_level: ExperienceLevel = ExperienceLevel.intermediate


class DiffChunk(BaseModel):
    file_path: str
    patch: str
    start_line: int | None = None
    end_line: int | None = None


class ReviewFinding(BaseModel):
    file_path: str
    line: int | None = None
    severity: Severity
    title: str
    explanation: str
    suggested_fix: str | None = None
    learning_resources: list[str] = Field(default_factory=list)


class Review(BaseModel):
    id: str
    context: PullRequestContext
    findings: list[ReviewFinding]
    summary: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
