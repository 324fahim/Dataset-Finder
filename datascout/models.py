from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum

class AccessType(str, Enum):
    OPEN = "open"
    AUTH_REQUIRED = "auth_required"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"

class DatasetRecord(BaseModel):
    id: str
    title: str
    description: str = "Unknown"
    source: str
    dataset_url: str
    download_url: Optional[str] = None
    formats: List[str] = Field(default_factory=list)
    size_bytes: Optional[int] = None
    records: Optional[int] = None
    features: Optional[int] = None
    license: str = "Unknown"
    last_updated: Optional[datetime] = None
    language: Optional[str] = None
    geography: Optional[str] = None
    ml_tasks: List[str] = Field(default_factory=list)
    access_type: AccessType = AccessType.UNKNOWN
    relevance_score: float = 0.0
    relevance_explanation: str = ""
    metadata_provenance: str = ""

class SearchRequest(BaseModel):
    raw_query: str
    topic: Optional[str] = None
    domain: Optional[str] = None
    preferred_format: Optional[str] = None
    ml_task: Optional[str] = None
    min_size_mb: Optional[float] = None
    license: Optional[str] = None

class SearchFilters(BaseModel):
    sources: List[str] = Field(default_factory=list)
    formats: List[str] = Field(default_factory=list)
    licenses: List[str] = Field(default_factory=list)
    ml_tasks: List[str] = Field(default_factory=list)
    access_types: List[AccessType] = Field(default_factory=list)
    sort_by: Literal["relevance","newest","largest","source"] = "relevance"