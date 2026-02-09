from callfunction import *

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 기술 개념을 쉬운 비유와 예시를 섞어서 설명하는 AI선생님이야."),
    ("user", "{question}"),
    ("ai", "질문에 대해 무엇인지, 왜 중요한지 예시를 섞어서 설명할게요")
])

chain = prompt | llm | StrOutputParser()

user_question = input("질문: ")
response = chain.invoke({"question":user_question})
print(response)