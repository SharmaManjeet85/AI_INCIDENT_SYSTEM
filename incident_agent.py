from langchain_core.prompts import ChatPromptTemplate
from llm import llm

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI SRE predicting production incidents."),
    ("human", """
Based on this anomaly report:

{report}

Predict:
- Probability of major incident (0-100%)
- Type of possible incident
- Recommended immediate action
""")
])

chain = prompt | llm

def predict_incident(report):
    response = chain.invoke({"report": report})
    return response.content
