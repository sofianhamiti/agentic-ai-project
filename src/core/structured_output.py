"""Model classes for structured output."""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    """Structured search result."""
    
    main_findings: str = Field(description="The main findings or answer to the search query")
    key_points: List[str] = Field(description="Key points found in the search")
    sources: List[str] = Field(description="References for the information", default_factory=list)
    confidence: int = Field(description="Confidence score (1-10)", ge=1, le=10)
    follow_up_questions: Optional[List[str]] = Field(description="Relevant follow-up questions", default=None) 