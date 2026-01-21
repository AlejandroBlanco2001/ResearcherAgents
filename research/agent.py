from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LoopAgent, SequentialAgent, ParallelAgent
from .models import Intention
from .tools import mcp_arxiv, mcp_google_scholar

from .prompts import (
    KEYWORD_AGENT_DESCRIPTION,
    KEYWORD_AGENT_INSTRUCTION,
    ARXIV_FINDER_AGENT_DESCRIPTION,
    ARXIV_FINDER_AGENT_INSTRUCTION,
    GOOGLE_SCHOLAR_FINDER_AGENT_DESCRIPTION,
    GOOGLE_SCHOLAR_FINDER_AGENT_INSTRUCTION,
    FINDER_AGENT_DESCRIPTION,
    RESUME_AGENT_DESCRIPTION,
    RESUME_AGENT_INSTRUCTION,
    RESEARCH_AGENT_DESCRIPTION,
    INTENTION_AGENT_DESCRIPTION,
    INTENTION_AGENT_INSTRUCTION,
    ROOT_AGENT_DESCRIPTION,
    ROOT_AGENT_INSTRUCTION,
    CRITIQUE_DIRECTOR_AGENT_DESCRIPTION,
    CRITIQUE_DIRECTOR_AGENT_INSTRUCTION,
    SOFT_CRITIQUE_AGENT_DESCRIPTION,
    SOFT_CRITIQUE_AGENT_INSTRUCTION,
    HARD_CRITIQUE_AGENT_DESCRIPTION,
    HARD_CRITIQUE_AGENT_INSTRUCTION,
    SUMMARIZE_ANSWER_AGENT_DESCRIPTION,
    SUMMARIZE_ANSWER_AGENT_INSTRUCTION,
)

model = LiteLlm(
    model="openai/gpt-4o-mini",
)

critque_model = LiteLlm(
    model="openai/gpt-4o",
)


keyword_agent = Agent(
    model=model,
    name="KeywordAgent",
    description=KEYWORD_AGENT_DESCRIPTION,
    instruction=KEYWORD_AGENT_INSTRUCTION,
)

arxiv_finder_agent = Agent(
    model=model,
    name="ArXivSearchAgent",
    description=ARXIV_FINDER_AGENT_DESCRIPTION,
    instruction=ARXIV_FINDER_AGENT_INSTRUCTION,
    tools=[mcp_arxiv],
)

google_scholar_finder_agent = Agent(
    model=model,
    name="GoogleScholarSearchAgent",
    description=GOOGLE_SCHOLAR_FINDER_AGENT_DESCRIPTION,
    instruction=GOOGLE_SCHOLAR_FINDER_AGENT_INSTRUCTION,
    tools=[mcp_google_scholar],
)

finder_agent = ParallelAgent(
    name="ParallelSearchAgent",
    description=FINDER_AGENT_DESCRIPTION,
    sub_agents=[
        arxiv_finder_agent,
        google_scholar_finder_agent,
    ],
)

resume_agent = Agent(
    model=model,
    name="ResumeAgent",
    description=RESUME_AGENT_DESCRIPTION,
    instruction=RESUME_AGENT_INSTRUCTION,
)

soft_critique_agent = Agent(
    model=critque_model,
    name="SoftCritiqueAgent",
    description=SOFT_CRITIQUE_AGENT_DESCRIPTION,
    instruction=SOFT_CRITIQUE_AGENT_INSTRUCTION,
)

hard_critique_agent = Agent(
    model=critque_model,
    name="HardCritiqueAgent",
    description=HARD_CRITIQUE_AGENT_DESCRIPTION,
    instruction=HARD_CRITIQUE_AGENT_INSTRUCTION,
)

# Run both critiques in parallel
parallel_critique_agent = ParallelAgent(
    name="ParallelCritiqueAgent",
    description="Run soft and hard critiques in parallel on the papers.",
    sub_agents=[
        soft_critique_agent,
        hard_critique_agent,
    ],
)

# LLM agent that reasons about and synthesizes both critiques
critique_director_agent = Agent(
    model=critque_model,
    name="CritiqueDirectorAgent",
    description=CRITIQUE_DIRECTOR_AGENT_DESCRIPTION,
    instruction=CRITIQUE_DIRECTOR_AGENT_INSTRUCTION,
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
    name="IntentionAgent",
    description=INTENTION_AGENT_DESCRIPTION,
    instruction=INTENTION_AGENT_INSTRUCTION,
    output_schema=Intention,
)

summarize_answer_agent = Agent(
    model=model,
    name="SummarizeAnswerAgent",
    description=SUMMARIZE_ANSWER_AGENT_DESCRIPTION,
    instruction=SUMMARIZE_ANSWER_AGENT_INSTRUCTION,
)

root_agent = SequentialAgent(
    name="RootAgent",
    description=ROOT_AGENT_DESCRIPTION,
    sub_agents=[
        intention_agent,
        research_agent,
        parallel_critique_agent,
        critique_director_agent
        summarize_answer_agent,
    ],
)
