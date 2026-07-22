"""Data models for scientific writer API responses."""

from collections.abc import Mapping
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


def _utc_now_iso() -> str:
    """Current UTC time as an ISO 8601 string with explicit offset."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ProgressUpdate:
    """Progress update during document generation.

    Attributes:
        type: Always "progress" to distinguish from result messages
        timestamp: ISO 8601 timestamp of the update
        message: Human-readable progress message
        stage: Current workflow stage (initialization|planning|research|writing|compilation|complete)
        details: Optional dictionary with additional context (tool name, files created, etc.)
    """
    type: str = "progress"
    timestamp: str = field(default_factory=_utc_now_iso)
    message: str = ""
    stage: str = "initialization"  # initialization|planning|research|writing|compilation|complete
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        # Remove details if None to keep output clean
        if result.get('details') is None:
            del result['details']
        return result


@dataclass
class TextUpdate:
    """Live text output from Scientific-Writer during document generation.

    Streams Scientific-Writer's actual text responses in real-time, allowing API consumers
    to display the AI's reasoning and explanations as they happen.

    Attributes:
        type: Always "text" to distinguish from progress and result messages
        content: The text content from Scientific-Writer's response
    """
    type: str = "text"
    content: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class PaperMetadata:
    """Metadata about the generated document."""
    title: str | None = None
    created_at: str = field(default_factory=_utc_now_iso)
    topic: str = ""
    word_count: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class PaperFiles:
    """File paths for generated document artifacts.

    PDF/TeX fields remain for backward compatibility. The generic artifact
    fields cover presentations, Word documents, Markdown, HTML, spreadsheets,
    and image-only outputs such as infographics.
    """

    pdf_final: str | None = None
    tex_final: str | None = None
    pdf_drafts: list[str] = field(default_factory=list)
    tex_drafts: list[str] = field(default_factory=list)
    bibliography: str | None = None
    figures: list[str] = field(default_factory=list)
    data: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    final_artifacts: list[str] = field(default_factory=list)
    draft_artifacts: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    progress_log: str | None = None
    summary: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class TokenUsage:
    """Token usage statistics.

    Attributes:
        input_tokens: Total input tokens consumed
        output_tokens: Total output tokens consumed
        cache_creation_input_tokens: Tokens used for cache creation
        cache_read_input_tokens: Tokens read from cache
    """
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        """Calculate total tokens (input + output)."""
        return self.input_tokens + self.output_tokens

    def add_usage(self, usage: Mapping[str, Any] | object | None) -> None:
        """Accumulate an SDK usage mapping or usage-like object."""
        if not usage:
            return

        def read(name: str) -> int:
            value = (
                usage.get(name, 0)
                if isinstance(usage, Mapping)
                else getattr(usage, name, 0)
            )
            return int(value or 0)

        self.input_tokens += read("input_tokens")
        self.output_tokens += read("output_tokens")
        self.cache_creation_input_tokens += read("cache_creation_input_tokens")
        self.cache_read_input_tokens += read("cache_read_input_tokens")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        result['total_tokens'] = self.total_tokens
        return result


@dataclass
class PaperResult:
    """Final result containing all information about the generated document."""
    type: str = "result"
    status: str = "success"  # success|partial|failed
    paper_directory: str = ""
    paper_name: str = ""
    metadata: PaperMetadata = field(default_factory=PaperMetadata)
    files: PaperFiles = field(default_factory=PaperFiles)
    citations: dict[str, Any] = field(default_factory=dict)
    figures_count: int = 0
    compilation_success: bool = False
    errors: list[str] = field(default_factory=list)
    token_usage: TokenUsage | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        # Ensure nested objects are also dictionaries
        if isinstance(self.metadata, PaperMetadata):
            result['metadata'] = self.metadata.to_dict()
        if isinstance(self.files, PaperFiles):
            result['files'] = self.files.to_dict()
        if isinstance(self.token_usage, TokenUsage):
            result['token_usage'] = self.token_usage.to_dict()
        elif self.token_usage is None:
            del result['token_usage']
        return result


# Document-neutral aliases for new integrations. The paper-prefixed names stay
# public to avoid breaking existing callers.
DocumentMetadata = PaperMetadata
DocumentFiles = PaperFiles
DocumentResult = PaperResult

