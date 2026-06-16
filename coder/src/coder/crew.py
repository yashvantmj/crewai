from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Coder():
    """Coder crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    agents: list[BaseAgent]
    tasks: list[Task]
    @agent
    def coder(self) -> Agent:
        return Agent(config=self.agents_config['coder'], 
                 verbose=True,
                 allow_code_execution=True,
                     max_execution_time=100,
                     max_retries=5,
                    )  # Set a maximum execution time for code execution)
    @task
    def coding_task(self) -> Task:
        return Task(config=self.tasks_config['coding_task'])
    
    def crew(self) -> Crew:
        """Creates the Coder crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        agents_list = getattr(self, 'agents', None)
        if not agents_list:
            agents_list = [self.coder()]

        tasks_list = getattr(self, 'tasks', None)
        if not tasks_list:
            tasks_list = [self.coding_task()]

        return Crew(
            agents=agents_list,
            tasks=tasks_list,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
