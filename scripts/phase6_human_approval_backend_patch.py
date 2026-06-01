from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

if "from typing import List, Literal" not in s:
    s = s.replace("from typing import List", "from typing import List, Literal")

if "class ApprovalAction" not in s:
    marker = '''class MCPToolFirewallDecision(BaseModel):
    tool: MCPTool
    status: Literal["allowed", "blocked", "requires_approval", "redacted", "escalated"]
    risk_tier: RiskTier
    reason: str
    rule_id: str


class MCPRequestRecord'''
    replacement = '''class MCPToolFirewallDecision(BaseModel):
    tool: MCPTool
    status: Literal["allowed", "blocked", "requires_approval", "redacted", "escalated"]
    risk_tier: RiskTier
    reason: str
    rule_id: str


class ApprovalAction(BaseModel):
    action: Literal["approve", "reject", "escalate"]
    reviewer: str = "Compliance Officer"
    note: str = "Reviewed in Phase 6 Human Approval Workspace"


class MCPRequestRecord'''
    if marker not in s:
        raise SystemExit("MCPToolFirewallDecision marker not found")
    s = s.replace(marker, replacement)

if "reviewer_action" not in s:
    marker = '''class MCPRequestRecord(MCPRequestCreate):
    request_id: str
    created_at: datetime
    policy_result: PolicyResult
    final_outcome: str


class DashboardSummary'''
    replacement = '''class MCPRequestRecord(MCPRequestCreate):
    request_id: str
    created_at: datetime
    policy_result: PolicyResult
    final_outcome: str
    reviewer: str | None = None
    reviewer_action: str | None = None
    reviewer_note: str | None = None
    reviewed_at: datetime | None = None


class DashboardSummary'''
    if marker not in s:
        raise SystemExit("MCPRequestRecord marker not found")
    s = s.replace(marker, replacement)

if 'Human reviewer rejected the MCP request.' not in s:
    marker = '''def evaluate_policy(request: MCPRequestCreate) -> PolicyResult:
    risk = calculate_risk(request)
'''
    replacement = '''def evaluate_policy(request: MCPRequestCreate) -> PolicyResult:
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
'''
    if marker not in s:
        raise SystemExit("evaluate_policy marker not found")
    s = s.replace(marker, replacement)

if "/api/mcp/requests/{request_id}/approval" not in s:
    marker = '''@app.get("/api/mcp/evidence/{request_id}", response_model=MCPRequestRecord)
def evidence(request_id: str):
    for record in REQUESTS:
        if record.request_id == request_id:
            return record

    raise HTTPException(status_code=404, detail="MCP request not found")


@app.get("/api/dashboard", response_model=DashboardSummary)'''
    replacement = '''@app.get("/api/mcp/evidence/{request_id}", response_model=MCPRequestRecord)
def evidence(request_id: str):
    for record in REQUESTS:
        if record.request_id == request_id:
            return record

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


@app.get("/api/dashboard", response_model=DashboardSummary)'''
    if marker not in s:
        raise SystemExit("evidence endpoint marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 6 backend approval patch applied")
