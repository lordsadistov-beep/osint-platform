from pydantic import BaseModel
import uuid


class ToolResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: str | None
    icon: str | None
    is_active: bool

    class Config:
        from_attributes = True


class UsernameSearchResult(BaseModel):
    site: str
    url: str
    profile_exists: bool
    avatar: str | None = None
    name: str | None = None


class UsernameSearchResponse(BaseModel):
    query: str
    sites_checked: int
    found: list[UsernameSearchResult]
    not_found_count: int
    elapsed_ms: int


class EmailCheckResponse(BaseModel):
    email: str
    gravatar: str | None = None
    breaches: list[str] = []
    associated_sites: list[str] = []
    domain_info: dict | None = None


class PhoneCheckResponse(BaseModel):
    phone: str
    country: str | None = None
    carrier: str | None = None
    possible_owner: str | None = None
    messengers: dict = {}
    breaches: list[str] = []


class DomainLookupResponse(BaseModel):
    domain: str
    whois: dict | None = None
    dns: dict | None = None
    ip: str | None = None
    ip_geo: dict | None = None
    ssl: dict | None = None
    subdomains: list[str] = []


class MetadataResponse(BaseModel):
    filename: str
    size: int
    type: str
    exif: dict = {}
    gps: dict | None = None
    created_date: str | None = None
    camera: str | None = None
    software: str | None = None


class LeakSearchRequest(BaseModel):
    query: str
    type: str = "email"


class LeakEntryResponse(BaseModel):
    email: str | None = None
    username: str | None = None
    password_hash: str | None = None
    password_plain: str | None = None
    source: str
    breach_name: str | None = None
    ip_address: str | None = None
    phone: str | None = None


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
    relationship: str | None = None


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class SaveConnectionRequest(BaseModel):
    source_type: str
    source_value: str
    target_type: str
    target_value: str
    relationship: str | None = None
