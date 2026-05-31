from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MyProjectCr():
    """MyProjectCr crew"""
    agents_config: str = 'config/agents.yaml'
    tasks_config: str = 'config/tasks.yaml' # Ensure the path matches your folder structure

    @agent
    def for_debater(self) -> Agent:
        return Agent(
            config=self.agents_config['for_debater'],
            verbose=True
        )

    @agent
    def against_debater(self) -> Agent:
        return Agent(
            config=self.agents_config['against_debater'],
            verbose=True
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config['judge'],
            verbose=True
        )

    @task
    def propose(self) -> Task:
        return Task(config=self.tasks_config['propose'])

    @task
    def oppose(self) -> Task:
        return Task(config=self.tasks_config['oppose'])

    @task
    def decide(self) -> Task:
        return Task(
            config=self.tasks_config['decide'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MyProjectCr crew"""
        return Crew(
            agents=self.agents, # Automatically created by @agent decorators
            tasks=self.tasks,   # Automatically created by @task decorators
            process=Process.sequential,
            verbose=True,
        )