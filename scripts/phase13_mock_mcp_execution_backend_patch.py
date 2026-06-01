from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()


def insert_after_class(source: str, class_name: str, addition: str) -> str:
    if addition.strip().splitlines()[0] in source:
        return source

    lines = source.splitlines()
    start = None

    for i, line in enumerate(lines):
        if line.startswith(f"class {class_name}"):
            start = i
            break

    if start is None:
        raise SystemExit(f"{class_name} not found")

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("class ") or lines[j].startswith("def ") or lines[j].startswith("@app."):
            end = j
            break

    return "\n".join(lines[:end] + ["", addition.strip(), ""] + lines[end:]) + "\n"


def insert_before(source: str, marker: str, addition: str) -> str:
    if addition.strip().splitlines()[0] in source:
        return source

    idx = source.find(marker)
    if idx == -1:
        raise SystemExit(f"marker not found: {marker}")

    return source[:idx] + addition.strip() + "\n\n\n" + source[idx:]


mock_model = '''
class MockMCPExecutionResult(BaseModel):
    execution_id: str
    request_id: str
    requested_tool: MCPTool
    execution_status: Literal["executed", "blocked", "requires_approval", "redacted", "escalated"]
    policy_decision: str
    firewall_status: str
    reason: str
    mock_result: dict | None = None
    evidence_record: MCPRequestRecord
'''

s = insert_after_class(s, "MCPRequestRecord", mock_model)


helper = '''
def value_of(item):
    return item.value if hasattr(item, "value") else str(item)


def build_mock_mcp_result(record: MCPRequestRecord, status: str) -> dict | None:
    if status in {"blocked", "requires_approval", "escalated"}:
        return None

    tool = value_of(record.requested_tool)

    if tool == "search_internal_docs":
        return {
            "tool": tool,
            "result_type": "mock_document_summary",
            "summary": "Found 3 governed internal documentation references. Sensitive content was not exposed.",
            "records_returned": 3,
            "data_boundary": "simulated_internal_docs",
        }

    if tool == "query_database":
        return {
            "tool": tool,
            "result_type": "mock_database_result",
            "summary": "Returned aggregate financial exposure metrics only.",
            "rows_returned": 2,
            "data_boundary": "simulated_aggregate_rows",
        }

    if tool == "read_customer_record":
        if status == "redacted":
            return {
                "tool": tool,
                "result_type": "mock_redacted_customer_record",
                "summary": "Customer profile available only as redacted governance-safe metadata.",
                "redacted_fields": ["name", "account_number", "contact", "transaction_history"],
                "data_boundary": "simulated_redacted_record",
            }

        return {
            "tool": tool,
            "result_type": "mock_customer_record_summary",
            "summary": "Customer profile summary returned after approval and policy validation.",
            "fields_returned": ["risk_segment", "case_status", "last_reviewed"],
            "data_boundary": "simulated_customer_record",
        }

    if tool == "create_ticket":
        return {
            "tool": tool,
            "result_type": "mock_ticket_created",
            "ticket_id": f"mock_ticket_{record.request_id[-6:]}",
            "summary": "Governed operational ticket created in simulated service desk.",
            "data_boundary": "simulated_service_ticket",
        }

    return {
        "tool": tool,
        "result_type": "mock_execution_result",
        "summary": "Mock MCP execution completed under governance controls.",
        "data_boundary": "simulated_tool",
    }
'''

if "def build_mock_mcp_result" not in s:
    if "def build_evidence_timeline" in s:
        s = insert_before(s, "def build_evidence_timeline", helper)
    elif "def seed" in s:
        s = insert_before(s, "def seed", helper)
    else:
        raise SystemExit("No safe helper insertion point found")


endpoint = '''
@app.post("/api/mcp/execute", response_model=MockMCPExecutionResult)
def execute_mock_mcp(request: MCPRequestCreate):
    record = create_record(request)
    firewall_decisions = evaluate_mcp_firewall(request)

    requested_tool = value_of(request.requested_tool)
    matching_firewall = next(
        (
            decision
            for decision in firewall_decisions
            if value_of(decision.tool) == requested_tool
        ),
        firewall_decisions[0] if firewall_decisions else None,
    )

    policy_decision = value_of(record.policy_result.decision)
    firewall_status = value_of(matching_firewall.status) if matching_firewall else "unknown"

    if policy_decision == "deny" or firewall_status == "blocked":
        execution_status = "blocked"
        reason = "Mock MCP execution blocked by policy or firewall controls."
    elif policy_decision == "approval_required" or firewall_status == "requires_approval":
        execution_status = "requires_approval"
        reason = "Mock MCP execution paused until human approval evidence exists."
    elif policy_decision == "escalate" or firewall_status == "escalated":
        execution_status = "escalated"
        reason = "Mock MCP execution escalated for additional governance review."
    elif policy_decision == "redact" or firewall_status == "redacted":
        execution_status = "redacted"
        reason = "Mock MCP execution returned only redacted governance-safe output."
    else:
        execution_status = "executed"
        reason = "Mock MCP execution completed after identity, policy, firewall, and evidence validation."

    mock_result = build_mock_mcp_result(record, execution_status)

    record.final_outcome = execution_status
    REQUESTS.insert(0, record)

    return MockMCPExecutionResult(
        execution_id=f"mock_exec_{uuid4().hex[:10]}",
        request_id=record.request_id,
        requested_tool=record.requested_tool,
        execution_status=execution_status,
        policy_decision=policy_decision,
        firewall_status=firewall_status,
        reason=reason,
        mock_result=mock_result,
        evidence_record=record,
    )
'''

if "/api/mcp/execute" not in s:
    if '@app.patch("/api/mcp/requests/{request_id}/approval"' in s:
        s = insert_before(s, '@app.patch("/api/mcp/requests/{request_id}/approval"', endpoint)
    else:
        s = s.rstrip() + "\n\n\n" + endpoint.strip() + "\n"

p.write_text(s)
print("Phase 13 backend mock MCP execution patch applied")
