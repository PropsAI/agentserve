import agentserve

app = agentserve.app()

@app.agent
def my_agent(task_data):
    return task_data

app.run()