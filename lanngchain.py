from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest


class Context(TypedDict):
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user role."""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "You are a helpful assistant."

    if user_role == "expert":
        return f"{base_prompt} Provide detailed technical responses."
    elif user_role == "beginner":
        return f"{base_prompt} Explain concepts simply and avoid jargon."

    return base_prompt

# Provide a simple stub for `web_search` if it's not defined elsewhere.
try:
    web_search
except NameError:
    web_search = {"name": "web_search", "description": "Stub web search tool"}

agent = create_agent(
    model="claude-3-haiku-20240307",
    tools=[web_search],
    middleware=[user_role_prompt],
    context_schema=Context,
)


if __name__ == "__main__":
    # The system prompt will be set dynamically based on context
    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": "Explain machine learning"}]},
            context={"user_role": "expert"},
        )
        print(result)
    except Exception as e:
        print("Agent invocation failed:", e)