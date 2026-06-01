from datetime import datetime, timezone
from enum import Enum
from typing import List, Literal
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


class RiskEvaluation(BaseModel):
    risk_tier: RiskTier
    risk_score: int
    risk_factors: List[str]
    protected_data: bool
    action_type: str


class PolicyPreview(BaseModel):
    requested_tool: MCPTool
    requested_resource: str
    data_classification: DataClassification
    risk_evaluation: RiskEvaluation
    policy_result: PolicyResult
    evaluated_controls: List[str]
    rule_id: str


class MCPToolFirewallDecision(BaseModel):
    tool: MCPTool
    status: Literal["allowed", "blocked", "requires_approval", "redacted", "escalated"]
    risk_tier: RiskTier
    reason: str
    rule_id: str


class ApprovalAction(BaseModel):
    action: Literal["approve", "reject", "escalate"]
    reviewer: str = "Compliance Officer"
    note: str = "Reviewed in Phase 6 Human Approval Workspace"


class EvidenceTimelineStep(BaseModel):
    step: str
    label: str
    status: str
    detail: str
    timestamp: datetime | None = None


class EvidenceTimeline(BaseModel):
    request_id: str
    requested_tool: MCPTool
    final_outcome: str
    steps: List[EvidenceTimelineStep]


class MCPRequestRecord(MCPRequestCreate):
    request_id: str
    created_at: datetime
    policy_result: PolicyResult
    final_outcome: str
    reviewer: str | None = None
    reviewer_action: str | None = None
    reviewer_note: str | None = None
    reviewed_at: datetime | None = None


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


def action_type_for_tool(tool: MCPTool) -> str:
    if tool == MCPTool.search_internal_docs:
        return "read_knowledge"
    if tool == MCPTool.query_database:
        return "query_structured_data"
    if tool == MCPTool.read_customer_record:
        return "read_sensitive_record"
    if tool == MCPTool.create_ticket:
        return "create_operational_record"
    return "unknown"


def evaluate_risk(request: MCPRequestCreate) -> RiskEvaluation:
    factors: list[str] = []
    score = 0

    protected_data = request.data_classification in {
        DataClassification.confidential,
        DataClassification.restricted,
        DataClassification.regulated,
    }

    if protected_data:
        score += 25
        factors.append(f"Protected data classification: {request.data_classification.value}")

    if request.requested_tool == MCPTool.search_internal_docs:
        score += 10
        factors.append("Low-impact MCP knowledge retrieval")

    if request.requested_tool == MCPTool.create_ticket:
        score += 20
        factors.append("Operational record creation")

    if request.requested_tool == MCPTool.query_database:
        score += 45
        factors.append("Structured enterprise data query")

    if request.requested_tool == MCPTool.read_customer_record:
        score += 60
        factors.append("Sensitive customer record access")

    if request.clearance_level < 3:
        score += 15
        factors.append("Requester clearance below confidential threshold")

    if request.clearance_level < 4 and request.data_classification in {
        DataClassification.restricted,
        DataClassification.regulated,
    }:
        score += 20
        factors.append("Requester clearance below restricted/regulated threshold")

    if request.environment_context not in {"demo", "staging", "approved_lab"}:
        score += 40
        factors.append("Environment context is not approved")

    if request.approval_status == "approved":
        score -= 15
        factors.append("Human approval evidence present")

    score = max(0, min(score, 100))

    if score >= 80:
        tier = RiskTier.tier_4_critical
    elif score >= 50:
        tier = RiskTier.tier_3_high
    elif score >= 20:
        tier = RiskTier.tier_2_moderate
    else:
        tier = RiskTier.tier_1_low

    return RiskEvaluation(
        risk_tier=tier,
        risk_score=score,
        risk_factors=factors,
        protected_data=protected_data,
        action_type=action_type_for_tool(request.requested_tool),
    )


def policy_rule_id(request: MCPRequestCreate, result: PolicyResult) -> str:
    return f"mcp.{request.requested_tool.value}.{request.data_classification.value}.{result.decision.value}"


def evaluated_controls_for(request: MCPRequestCreate, result: PolicyResult) -> list[str]:
    controls = [
        "identity_context_present",
        "role_declared",
        "department_declared",
        "business_purpose_declared",
        "environment_context_checked",
        "data_classification_checked",
        "mcp_tool_sensitivity_checked",
        "risk_tier_calculated",
        "policy_decision_recorded",
    ]

    if result.approval_required:
        controls.append("human_approval_required")

    if result.redaction_required:
        controls.append("redaction_required")

    if result.blocked:
        controls.append("execution_blocked")

    if request.approval_status == "approved":
        controls.append("approval_evidence_present")

    return controls


def build_policy_preview(request: MCPRequestCreate) -> PolicyPreview:
    result = evaluate_policy(request)
    return PolicyPreview(
        requested_tool=request.requested_tool,
        requested_resource=request.requested_resource,
        data_classification=request.data_classification,
        risk_evaluation=evaluate_risk(request),
        policy_result=result,
        evaluated_controls=evaluated_controls_for(request, result),
        rule_id=policy_rule_id(request, result),
    )


def firewall_status_for(result: PolicyResult) -> Literal["allowed", "blocked", "requires_approval", "redacted", "escalated"]:
    if result.decision == Decision.allow:
        return "allowed"

    if result.decision == Decision.deny:
        return "blocked"

    if result.decision == Decision.approval_required:
        return "requires_approval"

    if result.decision == Decision.redact:
        return "redacted"

    return "escalated"


def evaluate_mcp_firewall(request: MCPRequestCreate) -> list[MCPToolFirewallDecision]:
    decisions: list[MCPToolFirewallDecision] = []

    for tool in MCPTool:
        tool_request = request.model_copy(update={"requested_tool": tool})
        result = evaluate_policy(tool_request)

        decisions.append(
            MCPToolFirewallDecision(
                tool=tool,
                status=firewall_status_for(result),
                risk_tier=result.risk_tier,
                reason=result.reason,
                rule_id=policy_rule_id(tool_request, result),
            )
        )

    return decisions


def evaluate_policy(request: MCPRequestCreate) -> PolicyResult:
    risk = calculate_risk(request)

    if request.approval_status == "rejected":
        return PolicyResult(
            decision=Decision.deny,
            risk_tier=RiskTier.tier_4_critical,
            reason="Human reviewer rejected the MCP request.",
            blocked=True,
        )

    if request.approval_status == "escalated":
        return PolicyResult(
            decision=Decision.escalate,
            risk_tier=RiskTier.tier_4_critical,
            reason="Human reviewer escalated the MCP request for additional governance review.",
            approval_required=True,
        )

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


def build_evidence_timeline(record: MCPRequestRecord) -> EvidenceTimeline:
    approval_status = "not_required"

    if record.policy_result.approval_required:
        approval_status = "pending"

    if record.reviewer_action:
        approval_status = record.reviewer_action

    steps = [
        EvidenceTimelineStep(
            step="01",
            label="Request Intake",
            status="captured",
            detail=f"{record.user_identity} requested {record.requested_tool.value} for {record.business_purpose}.",
            timestamp=record.created_at,
        ),
        EvidenceTimelineStep(
            step="02",
            label="Identity Context",
            status="validated",
            detail=f"Role={record.role}; department={record.department}; business_unit={record.business_unit}; clearance={record.clearance_level}; agent={record.agent_identity}.",
            timestamp=record.created_at,
        ),
        EvidenceTimelineStep(
            step="03",
            label="Data Classification",
            status="classified",
            detail=f"Resource={record.requested_resource}; classification={record.data_classification.value}; environment={record.environment_context}.",
            timestamp=record.created_at,
        ),
        EvidenceTimelineStep(
            step="04",
            label="Risk Tiering",
            status=record.policy_result.risk_tier.value,
            detail=f"Calculated risk tier: {record.policy_result.risk_tier.value.replace('_', ' ')}.",
            timestamp=record.created_at,
        ),
        EvidenceTimelineStep(
            step="05",
            label="Policy Decision",
            status=record.policy_result.decision.value,
            detail=record.policy_result.reason,
            timestamp=record.created_at,
        ),
        EvidenceTimelineStep(
            step="06",
            label="Human Approval",
            status=approval_status,
            detail=(
                f"Reviewer={record.reviewer}; action={record.reviewer_action}; note={record.reviewer_note}"
                if record.reviewer_action
                else "No completed reviewer action recorded."
            ),
            timestamp=record.reviewed_at or record.created_at,
        ),
        EvidenceTimelineStep(
            step="07",
            label="Final Outcome",
            status=record.final_outcome,
            detail=f"Final governed MCP outcome: {record.final_outcome}.",
            timestamp=record.reviewed_at or record.created_at,
        ),
    ]

    return EvidenceTimeline(
        request_id=record.request_id,
        requested_tool=record.requested_tool,
        final_outcome=record.final_outcome,
        steps=steps,
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


@app.post("/api/policy/preview", response_model=PolicyPreview)
def policy_preview(request: MCPRequestCreate):
    return build_policy_preview(request)


@app.post("/api/mcp/firewall/preview", response_model=list[MCPToolFirewallDecision])
def mcp_firewall_preview(request: MCPRequestCreate):
    return evaluate_mcp_firewall(request)


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


@app.get("/api/mcp/evidence/{request_id}/timeline", response_model=EvidenceTimeline)
def evidence_timeline(request_id: str):
    for record in REQUESTS:
        if record.request_id == request_id:
            return build_evidence_timeline(record)

    raise HTTPException(status_code=404, detail="MCP request not found")


@app.patch("/api/mcp/requests/{request_id}/approval", response_model=MCPRequestRecord)
def review_mcp_request(request_id: str, action: ApprovalAction):
    for index, record in enumerate(REQUESTS):
        if record.request_id != request_id:
            continue

        next_status = {
            "approve": "approved",
            "reject": "rejected",
            "escalate": "escalated",
        }[action.action]

        updated_request = MCPRequestCreate(
            user_identity=record.user_identity,
            role=record.role,
            department=record.department,
            business_unit=record.business_unit,
            clearance_level=record.clearance_level,
            agent_identity=record.agent_identity,
            service_identity=record.service_identity,
            environment_context=record.environment_context,
            business_purpose=record.business_purpose,
            requested_tool=record.requested_tool,
            requested_resource=record.requested_resource,
            data_classification=record.data_classification,
            approval_status=next_status,
        )

        policy_result = evaluate_policy(updated_request)

        updated = MCPRequestRecord(
            **updated_request.model_dump(),
            request_id=record.request_id,
            created_at=record.created_at,
            policy_result=policy_result,
            final_outcome=policy_result.decision.value,
            reviewer=action.reviewer,
            reviewer_action=action.action,
            reviewer_note=action.note,
            reviewed_at=now(),
        )

        REQUESTS[index] = updated
        return updated

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
