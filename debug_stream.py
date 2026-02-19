from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent

@tool
def restart_service(service_name: str) -> str:
    """Restart a backend service by name."""
    return f"Service '{service_name}' restarted successfully."

llm = ChatAnthropic(model='claude-3-haiku-20240307', temperature=0)

agent = create_agent(
    model=llm,
    tools=[restart_service],
    system_prompt=SystemMessage(content='You are an SRE assistant.'),
    interrupt_before=['tools']
)

for event in agent.stream({'messages': [{'role': 'human', 'content': 'Restart payment-service'}]}, {'configurable': {'thread_id': '1'}}):
    print('Event keys:', list(event.keys()) if isinstance(event, dict) else type(event))
    if 'messages' in event:
        print('Messages:', len(event['messages']))
        for i, msg in enumerate(event['messages']):
            print(f'  Msg {i}: {type(msg).__name__}')
            if hasattr(msg, 'tool_calls'):
                print(f'    tool_calls: {msg.tool_calls}')
