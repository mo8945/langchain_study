from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import dotenv
dotenv.load_dotenv() 

model = ChatOpenAI(model="gpt-4o-mini")

chat_history = "사용자: 내 이름은 '홍진모'야. \n AI: 반가워요 진모님!" # 미리 언급한 문장을 저장.

prompt = ChatPromptTemplate.from_template("이전 대화:{history} \n 질문: {input}")
chain = prompt | model | StrOutputParser()

# 과거 내역을 한꺼번에 보냄 -> 이름을 물어보기 전에 누구인지 데이터값을 전달.
result = chain.invoke({"history":chat_history, "input":"내 이름이 뭔지 알아요?"})
print(f"수동 메모리 응답: {result}")