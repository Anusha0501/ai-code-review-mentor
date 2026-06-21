from pydantic import BaseModel, Field
from backend.app.domain.models import DiffChunk, ExperienceLevel, ReviewFinding, Severity
from backend.app.rag.retriever import Retriever


class ReviewGraphState(BaseModel):
    chunks: list[DiffChunk]
    developer_level: ExperienceLevel
    findings: list[ReviewFinding] = Field(default_factory=list)
    documentation: list[str] = Field(default_factory=list)
    summary: str = ""


class ReviewCoordinator:
    """Production-facing seam for LangGraph orchestration.

    The implementation is deterministic for local development and tests. In
    production, each method maps cleanly to a LangGraph node: reviewer,
    documentation, mentor, learning, and coordinator.
    """

    def __init__(self, retriever: Retriever) -> None:
        self.retriever = retriever

    async def run(self, state: ReviewGraphState) -> ReviewGraphState:
        state = await self._reviewer_node(state)
        state = await self._documentation_node(state)
        state = self._mentor_node(state)
        state = self._learning_node(state)
        return state

    async def _reviewer_node(self, state: ReviewGraphState) -> ReviewGraphState:
        for chunk in state.chunks:
            if "TODO" in chunk.patch or "except Exception" in chunk.patch:
                state.findings.append(
                    ReviewFinding(
                        file_path=chunk.file_path,
                        severity=Severity.warning,
                        title="Tighten implementation before merge",
                        explanation="The change includes a broad placeholder or broad exception handling that can hide production failures.",
                        suggested_fix="Replace placeholders with tracked follow-up work and catch specific exception types.",
                    )
                )
        return state

    async def _documentation_node(self, state: ReviewGraphState) -> ReviewGraphState:
        docs = await self.retriever.search("code review maintainability testing security")
        state.documentation = [f"{doc.title}: {doc.url}" for doc in docs]
        return state

    def _mentor_node(self, state: ReviewGraphState) -> ReviewGraphState:
        prefix = {
            ExperienceLevel.beginner: "Start with the underlying concept, then apply the fix.",
            ExperienceLevel.intermediate: "Focus on the tradeoff and the production impact.",
            ExperienceLevel.senior: "Prioritize risk, maintainability, and team conventions.",
        }[state.developer_level]
        for finding in state.findings:
            finding.explanation = f"{prefix} {finding.explanation}"
        return state

    def _learning_node(self, state: ReviewGraphState) -> ReviewGraphState:
        for finding in state.findings:
            finding.learning_resources.extend(state.documentation)
        state.summary = f"Generated {len(state.findings)} review finding(s) with mentoring context."
        return state
