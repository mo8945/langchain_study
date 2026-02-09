# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

from callfunction import *

import dotenv
dotenv.load_dotenv() 

prompt = ChatPromptTemplate.from_messages([
      ("system", """ 당신은 기술 개념을 쉬운 비유와 예시를 섞어서 설명하는 AI 선생님이야.
       사용자의 질문에 다음 세가지 요소를 포함하여 답변해주세요:
       1. 정의: 기술의 개념을 명확하게 설명
       2. 이유(중요성): 왜 이 기술을 사용하는지 설명
       3. 쉬운 예시: 일상생활의 비유를 들어 초보자도 이해하기 쉽게 설명 """),
      ("user","{question}")
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

parser = StrOutputParser()

chain = prompt | llm | parser

if __name__ == "__main__":
      input_data = {"question":"REST API란?"}
      response = chain.invoke(input_data)
      
      print("="*80)
      print(f"질문: {input_data['question']}")
      print("="*80)
      print(response)