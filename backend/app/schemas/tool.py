from pydantic import BaseModel
import uuid
from typing import Optional


class ToolResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: Optional[str]
    icon: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True


class UsernameSearchResult(BaseModel):
    site: str
    url: str
    profile_exists: bool
    avatar: Optional[str] = None
    name: Optional[str] = None


class UsernameSearchResponse(BaseModel):
    query: str
    sites_checked: int
    found: list[UsernameSearchResult]
    not_found_count: int
    elapsed_ms: int


class EmailCheckResponse(BaseModel):
    email: str
    gravatar: Optional[str] = None
    breaches: list[str] = []
    associated_sites: list[str] = []
    domain_info: Optional[dict] = None


class PhoneCheckResponse(BaseModel):
    phone: str
    country: Optional[str] = None
    carrier: Optional[str] = None
    possible_owner: Optional[str] = None
    messengers: dict = {}
    breaches: list[str] = []


class DomainLookupResponse(BaseModel):
    domain: str
    whois: Optional[dict] = None
    dns: Optional[dict] = None
    ip: Optional[str] = None
    ip_geo: Optional[dict] = None
    ssl: Optional[dict] = None
    subdomains: list[str] = []


class MetadataResponse(BaseModel):
    filename: str
    size: int
    type: str
    exif: dict = {}
    gps: Optional[dict] = None
    created_date: Optional[str] = None
    camera: Optional[str] = None
    software: Optional[str] = None


class LeakSearchRequest(BaseModel):
    query: str
    type: str = "email"


class LeakEntryResponse(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password_hash: Optional[str] = None
    password_plain: Optional[str] = None
    source: str
    breach_name: Optional[str] = None
    ip_address: Optional[str] = None
    phone: Optional[str] = None


class LeakSearchResponse(BaseModel):
    found: bool
    entries: list[LeakEntryResponse]
    total_count: int


class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    value: str


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: Optional[str] = None


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class SaveConnectionRequest(BaseModel):
    source_type: str
    source_value: str
    target_type: str
    target_value: str
    relationship: Optional[str] = None


