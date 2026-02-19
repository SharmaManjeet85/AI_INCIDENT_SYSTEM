from langchain_core.prompts import ChatPromptTemplate
from llm import llm

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior SRE log analysis expert."),
    ("human", """
Analyze the following logs.
Identify:
- error frequency
- unusual spikes
- suspicious patterns

Logs:
{logs}
""")
])

chain = prompt | llm

def analyze_logs(log_text):
    response = chain.invoke({"logs": log_text})
    return response.content
