from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

s = s.replace(
    "from typing import List",
    "from typing import List, Literal"
)

if "class MCPToolFirewallDecision" not in s:
    marker = '''class PolicyPreview(BaseModel):
    requested_tool: MCPTool
    requested_resource: str
    data_classification: DataClassification
    risk_evaluation: RiskEvaluation
    policy_result: PolicyResult
    evaluated_controls: List[str]
    rule_id: str


class MCPRequestRecord'''
    replacement = '''class PolicyPreview(BaseModel):
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


class MCPRequestRecord'''
    if marker not in s:
        raise SystemExit("PolicyPreview marker not found")
    s = s.replace(marker, replacement)

if "def firewall_status_for" not in s:
    marker = '''def build_policy_preview(request: MCPRequestCreate) -> PolicyPreview:
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
    replacement = '''def build_policy_preview(request: MCPRequestCreate) -> PolicyPreview:
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


def evaluate_policy'''
    if marker not in s:
        raise SystemExit("build_policy_preview marker not found")
    s = s.replace(marker, replacement)

if "/api/mcp/firewall/preview" not in s:
    marker = '''@app.post("/api/policy/preview", response_model=PolicyPreview)
def policy_preview(request: MCPRequestCreate):
    return build_policy_preview(request)
'''
    replacement = '''@app.post("/api/policy/preview", response_model=PolicyPreview)
def policy_preview(request: MCPRequestCreate):
    return build_policy_preview(request)


@app.post("/api/mcp/firewall/preview", response_model=list[MCPToolFirewallDecision])
def mcp_firewall_preview(request: MCPRequestCreate):
    return evaluate_mcp_firewall(request)
'''
    if marker not in s:
        raise SystemExit("policy preview endpoint marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 5 backend MCP firewall patch applied")
