from backend.app.domain.models import DiffChunk


class DiffChunker:
    """Splits GitHub patches into model-safe chunks.

    Why: models perform better when each request has a focused scope.
    Tradeoff: smaller chunks improve precision but can lose cross-file context.
    """

    def __init__(self, max_chars: int = 6_000) -> None:
        self.max_chars = max_chars

    def chunk(self, file_path: str, patch: str) -> list[DiffChunk]:
        if len(patch) <= self.max_chars:
            return [DiffChunk(file_path=file_path, patch=patch)]

        chunks: list[DiffChunk] = []
        current: list[str] = []
        current_size = 0
        for line in patch.splitlines():
            if current and current_size + len(line) > self.max_chars:
                chunks.append(DiffChunk(file_path=file_path, patch="\n".join(current)))
                current = []
                current_size = 0
            current.append(line)
            current_size += len(line) + 1
        if current:
            chunks.append(DiffChunk(file_path=file_path, patch="\n".join(current)))
        return chunks
