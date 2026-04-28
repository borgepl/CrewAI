 Here's a summary of what was created:

New files:

File	Purpose
strands_agent.py
The Strands agent — drop-in replacement for crew.py
requirements-strands.txt	Dependencies for the Strands version
Dockerfile.strands	Container build for the Strands agent
streamlitui_strands.py	Streamlit UI wired to the Strands agent
Modified:

agentcore.json
 — entrypoint updated to strands_agent.py
How the mapping works:

CrewAI	Strands
SerperDevTool	Custom @tool web_search using the same Serper API
vacation_researcher Agent (YAML config)	vacation_researcher = Agent(...) with system prompt
itinerary_planner Agent (YAML config)	itinerary_planner = Agent(...) with system prompt
Sequential Crew process	plan_vacation() function calling agents in sequence
LLM(model="bedrock/eu.amazon.nova-pro-v1:0")	BedrockModel(model_id="eu.amazon.nova-pro-v1:0")
@app.entrypoint (AgentCore)	Same @app.entrypoint pattern — fully compatible

## To run locally:

pip install strands-agents strands-agents-tools bedrock-agentcore
python src/vacation_planner/strands_agent.py --local Valencia

## To run as AgentCore service:

python src/vacation_planner/strands_agent.py
# Then: curl -X POST http://localhost:8080/invocations -H "Content-Type: application/json" -d '{"topic": "Paris"}'

## To run with Streamlit:
for Windows :
uv run streamlit run streamlitui_strands.py --server.headless true
for linux:
streamlit run streamlitui_strands.py
