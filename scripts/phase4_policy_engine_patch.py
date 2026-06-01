from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

if "class RiskEvaluation" not in s:
    marker = '''class PolicyResult(BaseModel):
    decision: Decision
    risk_tier: RiskTier
    reason: str
    approval_required: bool = False
    redaction_required: bool = False
    blocked: bool = False


class MCPRequestRecord'''
    replacement = '''class PolicyResult(BaseModel):
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


class MCPRequestRecord'''
    if marker not in s:
        raise SystemExit("PolicyResult marker not found")
    s = s.replace(marker, replacement)

if "def action_type_for_tool" not in s:
    marker = '''def calculate_risk(request: MCPRequestCreate) -> RiskTier:
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


def evaluate_policy'''
    replacement = '''def calculate_risk(request: MCPRequestCreate) -> RiskTier:
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


def evaluate_policy'''
    if marker not in s:
        raise SystemExit("calculate_risk marker not found")
    s = s.replace(marker, replacement)

if "/api/policy/preview" not in s:
    marker = '''@app.get("/api/mcp/tools", response_model=list[MCPToolDefinition])
def mcp_tools():
    return TOOLS
'''
    replacement = '''@app.get("/api/mcp/tools", response_model=list[MCPToolDefinition])
def mcp_tools():
    return TOOLS


@app.post("/api/policy/preview", response_model=PolicyPreview)
def policy_preview(request: MCPRequestCreate):
    return build_policy_preview(request)
'''
    if marker not in s:
        raise SystemExit("tools endpoint marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 4 backend patch applied")
