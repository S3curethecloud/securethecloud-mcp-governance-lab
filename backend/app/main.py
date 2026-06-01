from datetime import datetime, timezone
from enum import Enum
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


class DataClassification(str, Enum):
    public = "public"
    internal = "internal"
    confidential = "confidential"
    restricted = "restricted"
    regulated = "regulated"


class MCPTool(str, Enum):
    search_internal_docs = "search_internal_docs"
    query_database = "query_database"
    read_customer_record = "read_customer_record"
    create_ticket = "create_ticket"


class Decision(str, Enum):
    allow = "allow"
    deny = "deny"
    redact = "redact"
    approval_required = "approval_required"
    escalate = "escalate"


class RiskTier(str, Enum):
    tier_1_low = "tier_1_low"
    tier_2_moderate = "tier_2_moderate"
    tier_3_high = "tier_3_high"
    tier_4_critical = "tier_4_critical"


class MCPToolDefinition(BaseModel):
    name: MCPTool
    label: str
    description: str
    sensitivity: str
    default_risk_tier: RiskTier


class MCPRequestCreate(BaseModel):
    user_identity: str = Field(min_length=2)
    role: str
    department: str
    business_unit: str
    clearance_level: int = Field(ge=0, le=5)
    agent_identity: str = "securethecloud-demo-agent"
    service_identity: str = "mcp-lab-service"
    environment_context: str = "demo"
    business_purpose: str
    requested_tool: MCPTool
    requested_resource: str
    data_classification: DataClassification
    approval_status: str = "not_requested"


class PolicyResult(BaseModel):
    decision: Decision
    risk_tier: RiskTier
    reason: str
    approval_required: bool = False
    redaction_required: bool = False
    blocked: bool = False


class MCPRequestRecord(MCPRequestCreate):
    request_id: str
    created_at: datetime
    policy_result: PolicyResult
    final_outcome: str


class DashboardSummary(BaseModel):
    total_mcp_requests: int
    allowed_requests: int
    denied_requests: int
    approval_requests: int
    redacted_responses: int
    sensitive_access_attempts: int
    high_risk_activities: int
    policy_violations: int
    governance_coverage: int


class Health(BaseModel):
    status: str
    service: str
    lab_mode: bool
    phase: str


app = FastAPI(
    title="SecureTheCloud MCP Governance Lab API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


TOOLS: list[MCPToolDefinition] = [
    MCPToolDefinition(
        name=MCPTool.search_internal_docs,
        label="Search Internal Docs",
        description="Search internal enterprise knowledge repositories.",
        sensitivity="internal",
        default_risk_tier=RiskTier.tier_1_low,
    ),
    MCPToolDefinition(
        name=MCPTool.query_database,
        label="Query Database",
        description="Query structured enterprise data.",
        sensitivity="confidential",
        default_risk_tier=RiskTier.tier_3_high,
    ),
    MCPToolDefinition(
        name=MCPTool.read_customer_record,
        label="Read Customer Record",
        description="Read sensitive customer profile or account information.",
        sensitivity="restricted",
        default_risk_tier=RiskTier.tier_4_critical,
    ),
    MCPToolDefinition(
        name=MCPTool.create_ticket,
        label="Create Ticket",
        description="Create an operational service ticket.",
        sensitivity="internal",
        default_risk_tier=RiskTier.tier_2_moderate,
    ),
]

REQUESTS: list[MCPRequestRecord] = []


def now() -> datetime:
    return datetime.now(timezone.utc)


def calculate_risk(request: MCPRequestCreate) -> RiskTier:
    if request.data_classification in {
        DataClassification.regulated,
        DataClassification.restricted,
    }:
        return RiskTier.tier_4_critical

    if request.requested_tool in {
        MCPTool.query_database,
        MCPTool.read_customer_record,
    }:
        return RiskTier.tier_3_high

    if request.requested_tool == MCPTool.create_ticket:
        return RiskTier.tier_2_moderate

    if request.data_classification == DataClassification.confidential:
        return RiskTier.tier_2_moderate

    return RiskTier.tier_1_low


def evaluate_policy(request: MCPRequestCreate) -> PolicyResult:
    risk = calculate_risk(request)

    if request.environment_context not in {"demo", "staging", "approved_lab"}:
        return PolicyResult(
            decision=Decision.deny,
            risk_tier=RiskTier.tier_4_critical,
            reason="Environment context is not approved for MCP tool access.",
            blocked=True,
        )

    if request.requested_tool == MCPTool.read_customer_record:
        if request.clearance_level < 4:
            return PolicyResult(
                decision=Decision.deny,
                risk_tier=RiskTier.tier_4_critical,
                reason="Customer record access requires clearance level 4 or higher.",
                blocked=True,
            )

        if request.approval_status != "approved":
            return PolicyResult(
                decision=Decision.approval_required,
                risk_tier=RiskTier.tier_4_critical,
                reason="Customer record access requires human approval before MCP execution.",
                approval_required=True,
            )

        return PolicyResult(
            decision=Decision.allow,
            risk_tier=RiskTier.tier_4_critical,
            reason="Customer record access allowed after sufficient clearance and approval evidence.",
        )

    if request.requested_tool == MCPTool.query_database:
        if request.data_classification in {
            DataClassification.regulated,
            DataClassification.restricted,
        }:
            if request.approval_status != "approved":
                return PolicyResult(
                    decision=Decision.approval_required,
                    risk_tier=RiskTier.tier_4_critical,
                    reason="Restricted or regulated database query requires human approval.",
                    approval_required=True,
                )

        if request.clearance_level < 3:
            return PolicyResult(
                decision=Decision.redact,
                risk_tier=RiskTier.tier_3_high,
                reason="Database query may proceed only with redaction due to insufficient clearance.",
                redaction_required=True,
            )

        return PolicyResult(
            decision=Decision.allow,
            risk_tier=risk,
            reason="Database query satisfies role, clearance, and policy requirements.",
        )

    if request.requested_tool == MCPTool.create_ticket:
        if request.data_classification in {
            DataClassification.regulated,
            DataClassification.restricted,
        }:
            return PolicyResult(
                decision=Decision.redact,
                risk_tier=RiskTier.tier_2_moderate,
                reason="Ticket creation allowed only with sensitive content redacted.",
                redaction_required=True,
            )

        return PolicyResult(
            decision=Decision.allow,
            risk_tier=RiskTier.tier_2_moderate,
            reason="Ticket creation is permitted for low-impact operational metadata.",
        )

    if request.requested_tool == MCPTool.search_internal_docs:
        if request.data_classification == DataClassification.confidential:
            return PolicyResult(
                decision=Decision.redact,
                risk_tier=RiskTier.tier_2_moderate,
                reason="Internal document search may proceed with confidential content redacted.",
                redaction_required=True,
            )

        return PolicyResult(
            decision=Decision.allow,
            risk_tier=RiskTier.tier_1_low,
            reason="Internal documentation search is permitted for approved business purpose.",
        )

    return PolicyResult(
        decision=Decision.deny,
        risk_tier=RiskTier.tier_4_critical,
        reason="Requested MCP tool is not governed by the current policy set.",
        blocked=True,
    )


def create_record(request: MCPRequestCreate) -> MCPRequestRecord:
    policy_result = evaluate_policy(request)

    return MCPRequestRecord(
        **request.model_dump(),
        request_id=f"mcp_req_{uuid4().hex[:10]}",
        created_at=now(),
        policy_result=policy_result,
        final_outcome=policy_result.decision.value,
    )


def seed() -> None:
    if REQUESTS:
        return

    examples = [
        MCPRequestCreate(
            user_identity="Jordan Lee",
            role="Engineer",
            department="IT",
            business_unit="Infrastructure",
            clearance_level=2,
            business_purpose="Incident investigation",
            requested_tool=MCPTool.search_internal_docs,
            requested_resource="security runbooks",
            data_classification=DataClassification.internal,
        ),
        MCPRequestCreate(
            user_identity="Mina Patel",
            role="Support Analyst",
            department="Customer Operations",
            business_unit="Customer Trust",
            clearance_level=2,
            business_purpose="Resolve customer support case",
            requested_tool=MCPTool.read_customer_record,
            requested_resource="customer profile",
            data_classification=DataClassification.restricted,
        ),
        MCPRequestCreate(
            user_identity="Avery Chen",
            role="Risk Analyst",
            department="Finance",
            business_unit="Enterprise Risk",
            clearance_level=3,
            business_purpose="Quarterly risk reporting",
            requested_tool=MCPTool.query_database,
            requested_resource="financial exposure table",
            data_classification=DataClassification.confidential,
        ),
        MCPRequestCreate(
            user_identity="Taylor Morgan",
            role="Service Desk",
            department="IT",
            business_unit="Operations",
            clearance_level=1,
            business_purpose="Create incident ticket",
            requested_tool=MCPTool.create_ticket,
            requested_resource="service ticket",
            data_classification=DataClassification.internal,
        ),
    ]

    for item in examples:
        REQUESTS.append(create_record(item))


@app.on_event("startup")
def startup() -> None:
    seed()


@app.get("/health", response_model=Health)
def health():
    return Health(
        status="ok",
        service="securethecloud-mcp-governance-lab",
        lab_mode=True,
        phase="1",
    )


@app.get("/api/mcp/tools", response_model=list[MCPToolDefinition])
def mcp_tools():
    return TOOLS


@app.get("/api/mcp/requests", response_model=list[MCPRequestRecord])
def list_mcp_requests():
    return list(reversed(REQUESTS))


@app.post("/api/mcp/requests", response_model=MCPRequestRecord)
def submit_mcp_request(request: MCPRequestCreate):
    record = create_record(request)
    REQUESTS.append(record)
    return record


@app.get("/api/mcp/evidence/{request_id}", response_model=MCPRequestRecord)
def evidence(request_id: str):
    for record in REQUESTS:
        if record.request_id == request_id:
            return record

    raise HTTPException(status_code=404, detail="MCP request not found")


@app.get("/api/dashboard", response_model=DashboardSummary)
def dashboard():
    return DashboardSummary(
        total_mcp_requests=len(REQUESTS),
        allowed_requests=sum(r.policy_result.decision == Decision.allow for r in REQUESTS),
        denied_requests=sum(r.policy_result.decision == Decision.deny for r in REQUESTS),
        approval_requests=sum(r.policy_result.decision == Decision.approval_required for r in REQUESTS),
        redacted_responses=sum(r.policy_result.decision == Decision.redact for r in REQUESTS),
        sensitive_access_attempts=sum(
            r.data_classification
            in {
                DataClassification.confidential,
                DataClassification.restricted,
                DataClassification.regulated,
            }
            for r in REQUESTS
        ),
        high_risk_activities=sum(
            r.policy_result.risk_tier
            in {
                RiskTier.tier_3_high,
                RiskTier.tier_4_critical,
            }
            for r in REQUESTS
        ),
        policy_violations=sum(r.policy_result.decision == Decision.deny for r in REQUESTS),
        governance_coverage=100 if REQUESTS else 0,
    )
