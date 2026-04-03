from __future__ import annotations

import os
from crewai import Agent, Crew, Process, Task


class TenderAgentsAmp:
    """
    AMP-ready crew definition only.

    Implemented logic:
    1) The HITL task is explicitly marked as requiring human approval.
    2) The task instructions point to /webhooks/crewai-hitl using PUBLIC_BASE_URL.
    3) Workflow resume remains in the backend through /approvals/approve.

    Removed from this file because they are backend concerns:
    - CREWAI_BASE_URL
    - CREWAI_API_TOKEN
    - HITL_WEBHOOK_BEARER
    """

    def __init__(self) -> None:
        self.public_base_url = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

        self.research_agent = Agent(
            role="Purchase Request Researcher",
            goal="Collect the facts required for a purchase-approval decision.",
            backstory=(
                "You gather vendor details, cost, business purpose, urgency, "
                "risks, and a short recommendation for a manager."
            ),
            verbose=True,
        )

        self.approval_agent = Agent(
            role="Approval Pack Writer",
            goal="Prepare a clean approval pack for a human reviewer.",
            backstory=(
                "You convert the researcher findings into a concise pack that "
                "a manager can approve or reject quickly."
            ),
            verbose=True,
        )

    def crew(self) -> Crew:
        webhook_note = (
            f"When human approval is required, send the HITL request to: "
            f"{self.public_base_url}/webhooks/crewai-hitl"
            if self.public_base_url
            else "When human approval is required, send the HITL request to "
                 "the configured backend endpoint /webhooks/crewai-hitl."
        )

        collect_purchase_context = Task(
            description=(
                "Given a purchase request, summarize the requester, amount, "
                "vendor, purpose, urgency, and any known risks. "
                "Return a short structured summary.\n\n"
                "Use these inputs when available:\n"
                "- purchase_request_id\n"
                "- requester\n"
                "- vendor\n"
                "- amount_usd\n"
                "- currency\n"
                "- purpose\n"
                "- urgency\n"
                "- reviewer_user_id\n"
                "- reviewer_email"
            ),
            expected_output=(
                "A structured summary containing purchase_request_id, requester, "
                "vendor, amount_usd, currency, purpose, urgency, risk_notes, and recommendation."
            ),
            agent=self.research_agent,
        )

        prepare_human_review_pack = Task(
            description=(
                "Turn the structured summary into a manager-friendly review pack. "
                "Keep it concise and clear. Include what is being requested, why it is needed, "
                "the recommendation, and any review notes.\n\n"
                "This task requires Human-in-the-Loop approval.\n"
                f"{webhook_note}\n\n"
                "After the human approves from the backend approval screen, "
                "the backend endpoint /approvals/approve will resume the workflow."
            ),
            expected_output=(
                "A final approval pack containing request summary, recommendation, risk notes, "
                "and reviewer guidance, ready for human approval."
            ),
            agent=self.approval_agent,
        )

        return Crew(
            agents=[self.research_agent, self.approval_agent],
            tasks=[collect_purchase_context, prepare_human_review_pack],
            process=Process.sequential,
            verbose=True,
        )

    def kickoff_local_demo(self):
        inputs = {
            "purchase_request_id": "PR-1001",
            "requester": "Nora",
            "vendor": "Acme Analytics",
            "amount_usd": 18000,
            "currency": "USD",
            "purpose": "Annual BI license renewal",
            "urgency": "high",
            "reviewer_user_id": "manager-01",
            "reviewer_email": "manager@example.com",
        }
        return self.crew().kickoff(inputs=inputs)
