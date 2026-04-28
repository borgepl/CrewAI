"""
Strands Agents SDK - Vacation Planner Agent

Replaces the CrewAI-based vacation planner with Strands Agents SDK.
Uses the same Bedrock Nova Pro model and Serper web search tool,
deployed on Bedrock AgentCore Runtime.
"""

import os
import json
import urllib.request
import urllib.parse

from strands import Agent, tool
from strands.models import BedrockModel

# ---------- AgentCore imports --------------------
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

# ---------- Configuration --------------------
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "c00ce2ae93bd230c743bfe337b8cedec1122f241")

# ---------- Custom Tools --------------------

@tool
def web_search(query: str) -> str:
    """Search the web for current information about a topic using Google Search.

    Use this tool to find up-to-date information about travel destinations,
    tourist attractions, local foods, weather, events, and more.

    Args:
        query: The search query string to look up on the web.
    """
    try:
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": 10})
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        }

        req = urllib.request.Request(url, data=payload.encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))

        results = []

        # Collect answer box if present
        if "answerBox" in data:
            ab = data["answerBox"]
            if "answer" in ab:
                results.append(f"Answer: {ab['answer']}")
            elif "snippet" in ab:
                results.append(f"Answer: {ab['snippet']}")

        # Collect organic results
        for item in data.get("organic", [])[:8]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            results.append(f"- {title}: {snippet} ({link})")

        if not results:
            return f"No results found for: {query}"

        return "\n".join(results)

    except Exception as e:
        return f"Search error for '{query}': {str(e)}"


# ---------- Model Configuration --------------------

bedrock_model = BedrockModel(
    model_id="eu.amazon.nova-pro-v1:0",
    region_name="eu-west-1",
    max_tokens=4096,
    temperature=0.7,
)

# ---------- Agent Definitions --------------------

# Agent 1: Vacation Researcher - mirrors the CrewAI vacation_researcher agent
vacation_researcher = Agent(
    model=bedrock_model,
    tools=[web_search],
    system_prompt="""You are a Senior Vacation Researcher.

Your goal is to research and find the best vacation spots and information about a given travel destination.

You are a seasoned vacation researcher, known for your ability to discover hidden gems and unique experiences.
Your goal is to find unforgettable destinations tailored to a variety of travel interests.

When researching a destination:
- Search for the most interesting and relevant information
- Look for hidden gems, unique experiences, and must-see attractions
- Find information about local culture, history, and traditions
- Research local cuisine and must-try foods
- Look for practical travel tips and recommendations

Provide your findings as a detailed list of 15 bullet points highlighting the most important
and exciting facts about the destination.""",
)

# Agent 2: Itinerary Planner - mirrors the CrewAI itinerary_planner agent
itinerary_planner = Agent(
    model=bedrock_model,
    tools=[],
    system_prompt="""You are an Itinerary Planner.

Your goal is to create a detailed itinerary highlighting the best tourist spots,
including history of the city and a list of must-try local foods.

You are a meticulous planner with a keen eye for detail.
You specialize in crafting organized travel schedules and suggesting local culinary
experiences to make vacations truly memorable.

When creating an itinerary:
- Review the research findings provided to you
- Create a well-organized day-by-day travel plan
- Include historical context about the destination
- Highlight must-visit tourist attractions
- Create a comprehensive list of must-try local foods
- Add practical tips for each activity

Format your output as a detailed Markdown report (do NOT use triple backtick code blocks).
Include sections for: Overview, History, Day-by-Day Itinerary, Must-Try Local Foods, and Travel Tips.""",
)


def plan_vacation(destination: str) -> str:
    """Run the full vacation planning pipeline for a destination.

    Executes two agents sequentially:
    1. Vacation Researcher - researches the destination
    2. Itinerary Planner - creates a detailed itinerary from the research

    Args:
        destination: The travel destination to plan for.

    Returns:
        The final Markdown itinerary report.
    """
    print(f"[Step 1/2] Researching destination: {destination}")
    research_result = vacation_researcher(
        f"Conduct thorough research about the travel destination: {destination}. "
        f"Find interesting and relevant information to enrich the travel experience. "
        f"Provide a list of 15 bullet points highlighting the most important and exciting facts."
    )
    research_text = str(research_result)
    print(f"[Step 1/2] Research complete. Length: {len(research_text)} chars")

    print(f"[Step 2/2] Creating itinerary for: {destination}")
    itinerary_result = itinerary_planner(
        f"Review the following research findings about {destination} and create a detailed "
        f"travel report formatted in Markdown.\n\n"
        f"Research Findings:\n{research_text}\n\n"
        f"Create a fully fledged report summarizing key information about {destination}, "
        f"formatted in Markdown without using code block syntax (do not use triple backticks)."
    )
    report = str(itinerary_result)
    print(f"[Step 2/2] Itinerary complete. Length: {len(report)} chars")

    # Save report to file
    try:
        with open("report.md", "w") as f:
            f.write(report)
        print("Report saved to report.md")
    except Exception as e:
        print(f"Warning: Could not save report to file: {e}")

    return report


# ---------- AgentCore Entrypoint --------------------

@app.entrypoint
def agent_invocation(payload, context):
    """Handler for agent invocation on Bedrock AgentCore Runtime."""
    print(f"Payload: {payload}")
    try:
        # Extract destination from payload (compatible with existing API)
        destination = payload.get("topic", payload.get("prompt", "Valencia, Spain"))
        print(f"Processing vacation destination: {destination}")

        result = plan_vacation(destination)

        print("Context:\n-------\n", context)
        print("Result:\n*******\n", result[:500])

        return {"result": result}

    except Exception as e:
        print(f"Exception occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}


# ---------- Local Execution --------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--local":
        # Run locally without AgentCore
        destination = sys.argv[2] if len(sys.argv) > 2 else "Valencia"
        print(f"\n{'='*60}")
        print(f"  Vacation Planner (Strands Agent) - Local Mode")
        print(f"  Destination: {destination}")
        print(f"{'='*60}\n")
        result = plan_vacation(destination)
        print(f"\n{'='*60}")
        print("  FINAL REPORT")
        print(f"{'='*60}\n")
        print(result)
    else:
        # Run as AgentCore service
        app.run()
