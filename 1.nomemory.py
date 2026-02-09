from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import dotenv
dotenv.load_dotenv() 

model = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("{input}")
chain = prompt | model | StrOutputParser()

# 첫번째 질문
print(f"질문1: 내이름은 '테스트김'야 /응답:{chain.invoke({'input':'내이름은 테스트김이야.'})}")

# 두번째 질문
print(f"질문2: 내이름이 뭔지알아요? /응답:{chain.invoke({'input':'내이름이 뭔지알아요?'})}")
'''
질문1: 내이름은 '테스트김'야 /응답:안녕하세요, 테스트김님! 어떻게  도와드릴까요?
질문2: 내이름이 뭔지알아요? /응답:죄송하지만, 당신의 이름은 알 수  없습니다. 
      하지만 이야기하고 싶은 내용이 있다면 언제든지 말씀해 주세요!
'''