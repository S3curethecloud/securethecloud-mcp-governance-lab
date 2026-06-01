from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

if "class ExecutiveSummary" not in s:
    marker = '''class DashboardSummary(BaseModel):
    total_mcp_requests: int
    allowed_requests: int
    denied_requests: int
    approval_requests: int
    redacted_responses: int
    sensitive_access_attempts: int
    high_risk_activities: int
    policy_violations: int
    governance_coverage: int


class Health'''
    replacement = '''class DashboardSummary(BaseModel):
    total_mcp_requests: int
    allowed_requests: int
    denied_requests: int
    approval_requests: int
    redacted_responses: int
    sensitive_access_attempts: int
    high_risk_activities: int
    policy_violations: int
    governance_coverage: int


class ExecutiveSummary(BaseModel):
    readiness_posture: str
    readiness_reason: str
    total_mcp_requests: int
    sensitive_access_attempts: int
    high_risk_activities: int
    policy_violations: int
    pending_approvals: int
    completed_human_reviews: int
    risk_tier_1_low: int
    risk_tier_2_moderate: int
    risk_tier_3_high: int
    risk_tier_4_critical: int
    decisions_allow: int
    decisions_deny: int
    decisions_redact: int
    decisions_approval_required: int
    decisions_escalate: int
    firewall_allowed: int
    firewall_blocked: int
    firewall_requires_approval: int
    firewall_redacted: int
    firewall_escalated: int


class Health'''
    if marker not in s:
        raise SystemExit("DashboardSummary marker not found")
    s = s.replace(marker, replacement)

if "def executive_summary" not in s:
    marker = '''@app.get("/api/dashboard", response_model=DashboardSummary)
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
'''
    replacement = '''@app.get("/api/dashboard", response_model=DashboardSummary)
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


@app.get("/api/executive/summary", response_model=ExecutiveSummary)
def executive_summary():
    firewall_decisions = []
    for record in REQUESTS:
        request = MCPRequestCreate(
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
            approval_status=record.approval_status,
        )
        firewall_decisions.extend(evaluate_mcp_firewall(request))

    pending_approvals = sum(r.policy_result.decision == Decision.approval_required for r in REQUESTS)
    policy_violations = sum(r.policy_result.decision == Decision.deny for r in REQUESTS)
    high_risk = sum(
        r.policy_result.risk_tier in {RiskTier.tier_3_high, RiskTier.tier_4_critical}
        for r in REQUESTS
    )
    sensitive_attempts = sum(
        r.data_classification in {
            DataClassification.confidential,
            DataClassification.restricted,
            DataClassification.regulated,
        }
        for r in REQUESTS
    )
    completed_reviews = sum(r.reviewer_action is not None for r in REQUESTS)

    if pending_approvals > 0:
        posture = "Review Required"
        reason = "Human approval queue requires attention before MCP execution is allowed."
    elif policy_violations > 0:
        posture = "Guarded"
        reason = "Policy violations were blocked and captured as governance evidence."
    elif high_risk > 0:
        posture = "Controlled"
        reason = "High-risk MCP activity exists but is governed by policy and evidence controls."
    else:
        posture = "Demo Ready"
        reason = "No pending approval queue or unhandled high-risk decision pressure."

    return ExecutiveSummary(
        readiness_posture=posture,
        readiness_reason=reason,
        total_mcp_requests=len(REQUESTS),
        sensitive_access_attempts=sensitive_attempts,
        high_risk_activities=high_risk,
        policy_violations=policy_violations,
        pending_approvals=pending_approvals,
        completed_human_reviews=completed_reviews,
        risk_tier_1_low=sum(r.policy_result.risk_tier == RiskTier.tier_1_low for r in REQUESTS),
        risk_tier_2_moderate=sum(r.policy_result.risk_tier == RiskTier.tier_2_moderate for r in REQUESTS),
        risk_tier_3_high=sum(r.policy_result.risk_tier == RiskTier.tier_3_high for r in REQUESTS),
        risk_tier_4_critical=sum(r.policy_result.risk_tier == RiskTier.tier_4_critical for r in REQUESTS),
        decisions_allow=sum(r.policy_result.decision == Decision.allow for r in REQUESTS),
        decisions_deny=sum(r.policy_result.decision == Decision.deny for r in REQUESTS),
        decisions_redact=sum(r.policy_result.decision == Decision.redact for r in REQUESTS),
        decisions_approval_required=sum(r.policy_result.decision == Decision.approval_required for r in REQUESTS),
        decisions_escalate=sum(r.policy_result.decision == Decision.escalate for r in REQUESTS),
        firewall_allowed=sum(d.status == "allowed" for d in firewall_decisions),
        firewall_blocked=sum(d.status == "blocked" for d in firewall_decisions),
        firewall_requires_approval=sum(d.status == "requires_approval" for d in firewall_decisions),
        firewall_redacted=sum(d.status == "redacted" for d in firewall_decisions),
        firewall_escalated=sum(d.status == "escalated" for d in firewall_decisions),
    )
'''
    if marker not in s:
        raise SystemExit("dashboard endpoint marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 8 backend executive dashboard patch applied")
