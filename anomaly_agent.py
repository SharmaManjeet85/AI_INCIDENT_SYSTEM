from langchain_core.prompts import ChatPromptTemplate
from llm import llm

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an anomaly detection expert."),
    ("human", """
Based on this log summary:

{summary}

Determine:
- Is there an anomaly? (Yes/No)
- Why?
- Risk level (Low/Medium/High)
""")
])

chain = prompt | llm

def detect_anomaly(summary):
    response = chain.invoke({"summary": summary})
    return response.content
