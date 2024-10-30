import agentserve
from openai import OpenAI

app = agentserve.app()

@app.agent
def my_custom_agent(task_data):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": task_data["prompt"]}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    app.run()