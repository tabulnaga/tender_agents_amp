from __future__ import annotations

import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class TenderAgentsAmp:
    """
    CrewAI AMP-compatible crew definition.

    Logic implemented:
    1) In HITL, workflow should call /webhooks/crewai-hitl
    2) Backend /approvals/approve resumes the workflow
    """

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            role="Purchase Request Researcher",
            goal="Collect the facts required for a purchase-approval decision.",
            backstory=(
                "You gather vendor details, cost, business purpose, urgency, "
                "risks, and a short recommendation for a manager."
            ),
            verbose=True,
        )

    @agent
    def approval_agent(self) -> Agent:
        return Agent(
            role="Approval Pack Writer",
            goal="Prepare a clean approval pack for a human reviewer.",
            backstory=(
                "You convert the researcher findings into a concise pack that "
                "a manager can approve or reject quickly."
            ),
            verbose=True,
        )

    @task
    def collect_purchase_context(self) -> Task:
        return Task(
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
            agent=self.research_agent(),
        )

    @task
    def prepare_human_review_pack(self) -> Task:
        public_base_url = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

        webhook_note = (
            f"When human approval is required, send the HITL request to: "
            f"{public_base_url}/webhooks/crewai-hitl"
            if public_base_url
            else "When human approval is required, send the HITL request to "
                 "the configured backend endpoint /webhooks/crewai-hitl."
        )

        return Task(
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
            agent=self.approval_agent(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.research_agent(), self.approval_agent()],
            tasks=[self.collect_purchase_context(), self.prepare_human_review_pack()],
            process=Process.sequential,
            verbose=True,
        )