"""Data models for scientific writer API responses."""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime


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
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    message: str = ""
    stage: str = "initialization"  # initialization|planning|research|writing|compilation|complete
    details: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class PaperMetadata:
    """Metadata about the generated paper."""
    title: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    topic: str = ""
    word_count: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class PaperFiles:
    """File paths for all generated paper artifacts."""
    pdf_final: Optional[str] = None
    tex_final: Optional[str] = None
    pdf_drafts: List[str] = field(default_factory=list)
    tex_drafts: List[str] = field(default_factory=list)
    bibliography: Optional[str] = None
    figures: List[str] = field(default_factory=list)
    data: List[str] = field(default_factory=list)
    progress_log: Optional[str] = None
    summary: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        result['total_tokens'] = self.total_tokens
        return result


@dataclass
class PaperResult:
    """Final result containing all information about the generated paper."""
    type: str = "result"
    status: str = "success"  # success|partial|failed
    paper_directory: str = ""
    paper_name: str = ""
    metadata: PaperMetadata = field(default_factory=PaperMetadata)
    files: PaperFiles = field(default_factory=PaperFiles)
    citations: Dict[str, Any] = field(default_factory=dict)
    figures_count: int = 0
    compilation_success: bool = False
    errors: List[str] = field(default_factory=list)
    token_usage: Optional[TokenUsage] = None
    
    def to_dict(self) -> Dict[str, Any]:
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

