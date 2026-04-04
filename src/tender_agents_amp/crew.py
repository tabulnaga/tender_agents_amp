from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class TenderAgentsAmp:
    """TenderAgentsAmp crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["research_agent"],
            verbose=True,
        )

    @agent
    def approval_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["approval_agent"],
            verbose=True,
        )

    @task
    def collect_purchase_context(self) -> Task:
        return Task(
            config=self.tasks_config["collect_purchase_context"],
        )

    @task
    def prepare_human_review_pack(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_human_review_pack"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TenderAgentsAmp crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
