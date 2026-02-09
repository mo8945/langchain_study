# from callfunction import ChatOpenAI, ChatPromptTemplate, StrOutputParser, dotenv
# 모듈내에 들어가 있는 모든요소 (클래스, 함수,,,)
from callfunction import *
 
# 다른 모듈
from langchain_core.prompts import MessagesPlaceholder # 여러 메세지를 한꺼번에 삽입하는 역할
from langchain_core.messages import HumanMessage, AIMessage


model = ChatOpenAI(model="gpt-4o-mini")

# 프롬프트 설계(매개변수명은 변경불가)
prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 사용자의 이전 대화를 기억하는 전문 비서입니다."),
    MessagesPlaceholder(variable_name="chat_history"), # chat_history라는 변수에 들어있는 다양한 메세지리스트들을 위치에 넣어줌
    ("user","{input}")
])
chain = prompt | model | StrOutputParser()

# 대화를 했을때 기록을 저장할 수 있도록 저장 리스트만듦.
# exit문장을 만나기 전까지 계속해서 저장.
chat_history = [] # HumanMessage, AImessage 기록리스트

print("대화를 시작합니다. 종료하려면 'exit'를 입력요망!")

while True:
    user_input = input("사용자: ")
    
    if user_input.lower() == "exit":
        break
    response = chain.invoke({
        "input":user_input, # 현재질문
        "chat_history":chat_history #이전 대화 전체 전달
    })
    print("AI:", response)
    #대화 기록 누적 => 사용자 질문과 AI대답 문자열이 다름 구분해서 저장후 구분해서 관리
    Hu = HumanMessage(content=user_input)
    chat_history.append(Hu)
    Ai = AIMessage(content=response)
    chat_history.append(Ai)
    
    # chat_history.append(HumanMessage(content=user_input))
    # chat_history.append(AIMessage(content=response))
