from __future__ import annotations

import os
from crewai import Agent, Crew, Process
from crewai.project import CrewBase, agent, crew


@CrewBase
class TenderAgentsAmp:

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            role="Purchase Request Researcher",
            goal="Collect the facts required for a purchase-approval decision.",
            backstory="You gather vendor details, cost, business purpose, urgency, risks.",
            verbose=True,
        )

    @agent
    def approval_agent(self) -> Agent:
        return Agent(
            role="Approval Pack Writer",
            goal="Prepare a clean approval pack for a human reviewer.",
            backstory="You convert findings into a concise approval pack.",
            verbose=True,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.research_agent(), self.approval_agent()],
            process=Process.sequential,
            verbose=True,
        )