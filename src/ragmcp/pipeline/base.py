"""RAG Pipeline component base abstractions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class Document:
    """A parsed document with text content and metadata.

    Attributes:
        text: The document text content (e.g., markdown, plain text).
        metadata: Additional information about the document (source, page, etc.).
    """

    text: str
    metadata: dict[str, Any]


@dataclass
class Chunk:
    """A chunk of a document with position information.

    Attributes:
        text: The chunk text content.
        metadata: Metadata including source, position, and other context.
    """

    text: str
    metadata: dict[str, Any]


class Loader(ABC):
    """Abstract base class for document loader implementations.

    Provides unified interface for parsing various document formats
    (PDF, Markdown, Code, etc.) into a standardized Document format.
    """

    @abstractmethod
    def load(self, file_path: str) -> Document:
        """Load and parse a document file.

        Args:
            file_path: Path to the document file.

        Returns:
            A Document containing parsed text and metadata.
        """
        ...


class Splitter(ABC):
    """Abstract base class for document splitter implementations.

    Provides unified interface for splitting documents into chunks
    while preserving position information and context.
    """

    @abstractmethod
    def split(self, document: Document) -> list[Chunk]:
        """Split a document into chunks.

        Args:
            document: The Document to split.

        Returns:
            A list of Chunk objects with positioning metadata.
        """
        ...
