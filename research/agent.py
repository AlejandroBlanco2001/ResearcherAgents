from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import SequentialAgent, ParallelAgent
from .models import Intention
from .tools import mcp_arxiv, mcp_google_scholar
from prompts import *
model = LiteLlm(
    model='openai/gpt-4o-mini',
)


keyword_agent = Agent(
    model=model,
    name="keyword_agent",
    description=KEYWORD_AGENT_DESCRIPTION,
    instruction=KEYWORD_AGENT_INSTRUCTION,
)

arxiv_finder_agent = Agent(
    model=model,
    name="arxiv_finder_agent",
    description=ARXIV_FINDER_AGENT_DESCRIPTION,
    instruction=ARXIV_FINDER_AGENT_INSTRUCTION,
    tools=[mcp_arxiv],
)

google_scholar_finder_agent = Agent(
    model=model,
    name="google_scholar_finder_agent",
    description=GOOGLE_SCHOLAR_FINDER_AGENT_DESCRIPTION,
    instruction=GOOGLE_SCHOLAR_FINDER_AGENT_INSTRUCTION,
    tools=[mcp_google_scholar],
)

finder_agent = ParallelAgent(
    name="ParallelFinderAgent",
    description=FINDER_AGENT_DESCRIPTION,
    sub_agents=[
        arxiv_finder_agent,
        google_scholar_finder_agent,
    ],
)

resume_agent = Agent(
    model=model,
    name="resume_agent",
    description=RESUME_AGENT_DESCRIPTION,
    instruction=RESUME_AGENT_INSTRUCTION,
)


research_agent = SequentialAgent(
    name="ResearchAgent",
    description=RESEARCH_AGENT_DESCRIPTION,
    sub_agents=[
        keyword_agent,
        finder_agent,
        resume_agent,
    ],
)

intention_agent = Agent(
    model=model,
    name='intention_agent',
    description=INTENTION_AGENT_DESCRIPTION,
    instruction=INTENTION_AGENT_INSTRUCTION,
    output_schema=Intention,
    sub_agents=[research_agent],
)

root_agent = Agent(
    model=model,
    name='root_agent',
    description=ROOT_AGENT_DESCRIPTION,
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[intention_agent],
)
