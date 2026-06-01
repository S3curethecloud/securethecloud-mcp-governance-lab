from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

if "class EvidenceTimelineStep" not in s:
    marker = '''class ApprovalAction(BaseModel):
    action: Literal["approve", "reject", "escalate"]
    reviewer: str = "Compliance Officer"
    note: str = "Reviewed in Phase 6 Human Approval Workspace"


class MCPRequestRecord'''
    replacement = '''class ApprovalAction(BaseModel):
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


class MCPRequestRecord'''
    if marker not in s:
        raise SystemExit("ApprovalAction marker not found")
    s = s.replace(marker, replacement)

if "def build_evidence_timeline" not in s:
    marker = '''def create_record(request: MCPRequestCreate) -> MCPRequestRecord:
    policy_result = evaluate_policy(request)

    return MCPRequestRecord(
        **request.model_dump(),
        request_id=f"mcp_req_{uuid4().hex[:10]}",
        created_at=now(),
        policy_result=policy_result,
        final_outcome=policy_result.decision.value,
    )


def seed() -> None:'''
    replacement = '''def create_record(request: MCPRequestCreate) -> MCPRequestRecord:
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


def seed() -> None:'''
    if marker not in s:
        raise SystemExit("create_record marker not found")
    s = s.replace(marker, replacement)

if "/api/mcp/evidence/{request_id}/timeline" not in s:
    marker = '''@app.get("/api/mcp/evidence/{request_id}", response_model=MCPRequestRecord)
def evidence(request_id: str):
    for record in REQUESTS:
        if record.request_id == request_id:
            return record

    raise HTTPException(status_code=404, detail="MCP request not found")


@app.patch("/api/mcp/requests/{request_id}/approval", response_model=MCPRequestRecord)'''
    replacement = '''@app.get("/api/mcp/evidence/{request_id}", response_model=MCPRequestRecord)
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


@app.patch("/api/mcp/requests/{request_id}/approval", response_model=MCPRequestRecord)'''
    if marker not in s:
        raise SystemExit("evidence endpoint marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 7 backend evidence timeline patch applied")
