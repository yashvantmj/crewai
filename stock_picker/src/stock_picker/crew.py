from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from typing import List

import os
from pathlib import Path
from dotenv import load_dotenv

from crewai.memory import Memory


# Load .env from root directory (/workspaces/crewai/.env)
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

# Verify it loaded
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")
else:
    print("✓ API Key loaded successfully")

try:
    from crewai_tools import SerperDevTool
except ImportError:
    SerperDevTool = None

from .tools.push_tool import PushNotificationTool


class TrendingCompany(BaseModel):
    """ A company that is in the news and attracting attention """
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """ List of multiple trending companies that are in the news """
    companies: List[TrendingCompany] = Field(description="List of companies trending in the news")

class TrendingCompanyResearch(BaseModel):
    """ Detailed research on a company """
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for " \
    "investment")

class TrendingCompanyResearchList(BaseModel):
    """ A list of detailed research on all the companies """
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all " \
    "trending companies")

@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'], 
                     tools=[SerperDevTool()] if SerperDevTool else [],memory =True)
        

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], 
                     tools=[SerperDevTool()] if SerperDevTool else [])

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'],
                     tools=[PushNotificationTool()],memory =True)

    @task
    def find_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['find_trending_companies'], 
                    output_pydantic=TrendingCompanyList)
    @task
    def research_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['research_trending_companies'], 
                    output_pydantic=TrendingCompanyResearchList)
    @task
    def pick_stocks(self) -> Task:
        return Task(config=self.tasks_config['pick_best_company'], 
                    output_file='stock_picks.txt')
    @crew
    def crew(self):
        """Creates the StockPicker crew"""
        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True)
        
        memory_backend = Memory(
            storage='lancedb',
            root_scope='stock_picker',
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=memory_backend,
        )
