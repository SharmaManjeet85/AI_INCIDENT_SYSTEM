from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver


# ----------------------------
# Tool
# ----------------------------
@tool
def restart_service(service_name: str) -> str:
    """Restart a backend service by name."""
    return f"Service '{service_name}' restarted successfully."


# ----------------------------
# LLM (Anthropic)
# ----------------------------
llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0
)


# ----------------------------
# Agent (with human-in-the-loop middleware)
# ----------------------------
memory = MemorySaver()

agent = create_agent(
    model=llm,
    tools=[restart_service],
    system_prompt=SystemMessage(content="""
You are a Site Reliability Engineering (SRE) assistant.
You may use tools to perform actions.
Sensitive actions MUST go through human approval.
"""),
    interrupt_before=["tools"],
    checkpointer=memory
)


# ----------------------------
# Run Agent with human approval loop
# ----------------------------
messages = [
    {"role": "human", "content": "Restart the payment-service"}
]

config = {"configurable": {"thread_id": "1"}}
interrupted = False

# Stream the agent execution
for event in agent.stream({"messages": messages}, config):
    # Check for interrupt (human approval point)
    if "__interrupt__" in event:
        interrupted = True
        
        # Get the current state
        state = agent.get_state(config)
        if state and state.values and "messages" in state.values:
            msgs = state.values["messages"]
            if msgs:
                last_msg = msgs[-1]
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    print(f"\n*** HUMAN APPROVAL REQUIRED ***")
                    for tool_call in last_msg.tool_calls:
                        print(f"Tool: {tool_call['name']}")
                        print(f"Args: {tool_call['args']}")
                    
                    decision = input("Approve execution? (yes/no): ").strip().lower()
                    if decision != "yes":
                        print("Execution denied by human.")
                        break

# If interrupted and approved, resume
if interrupted:
    print("\nResuming execution...")
    for event in agent.stream(None, config):
        pass
    
    # Get final state
    final_state = agent.get_state(config)
    if final_state and final_state.values and "messages" in final_state.values:
        msgs = final_state.values["messages"]
        if msgs and hasattr(msgs[-1], "content"):
            print(f"\nFinal response: {msgs[-1].content}")

