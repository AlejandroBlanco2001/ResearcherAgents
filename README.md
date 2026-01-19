# Deep Research - Multi-Agent Research System

A multi-agent research system built with Google ADK that automates academic paper discovery, search, and summarization using parallel agents.

## Overview

The system uses a hierarchical agent architecture to:
1. Understand user intent
2. Generate search keywords
3. Search ArXiv and Google Scholar in parallel
4. Summarize relevant papers

## Architecture

```
root_agent
  └── intention_agent
        └── research_agent (SequentialAgent)
              ├── keyword_agent
              ├── finder_agent (ParallelAgent)
              │     ├── arxiv_finder_agent
              │     └── google_scholar_finder_agent
              └── resume_agent
```

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- OpenAI API key

### Installation

```bash
git clone <repository-url>
cd deep_research
uv sync
```

Create a `.env` file:
```env
OPENAI_API_KEY=your_api_key_here
```

## Usage

We encourage using the ADK web interface to run the application:

```bash
uv run adk web
```

Alternatively, you can use it programmatically:

```python
from research.agent import root_agent

response = root_agent.run("What are the latest developments in transformer architectures?")
print(response)
```

## Technology Stack

- Google ADK - Multi-agent system framework
- LiteLLM - LLM provider interface
- MCP - Model Context Protocol for tools
- Pydantic - Data validation

## Project Structure

```
deep_research/
├── main.py
├── research/
│   ├── agent.py      # Agent definitions
│   ├── models.py     # Pydantic models
│   └── tools.py      # MCP tool configs
└── pyproject.toml
```

## Workshop Objectives

Demonstrates:
- Multi-agent orchestration
- Parallel and sequential agent workflows
- MCP tool integration
- Structured outputs with Pydantic can run 