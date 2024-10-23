# main.py

from agentserve import AgentServer
{{AGENT_IMPORT}}

agent_server = AgentServer({{AGENT_CLASS}})
app = agent_server.app
