from callfunction import *
 
# 2. 새로운 클래스 로딩
from langchain_core.chat_history import InMemoryChatMessageHistory # 메모리 저장 객체(세션별 대화 기록 저장)
from langchain_core.runnables.history import RunnableWithMessageHistory # 세션별 대화 기록을 관리하는 래퍼
from langchain_core.messages import HumanMessage # 사용자 메시지를 표현하는 객체 (=UserMessage)

# 3. 모델 설정
model = ChatOpenAI(model="gpt-4o-mini")

# 4. 세션 저장소를 생성
store = {} # 세션별로 대화 기록을 저장할 딕셔너리(초기화)

# 5. 세션별 history를 반환(=보고) 함수 (매개변수 O, 반환값 O)=>직원
def get_session_history(session_id:str): # 매개변수명: 자료형(=문자인지, 숫자인지, 객체인지 알려주는 역할)
    # 저장 O or X => if 조건문을 사용
    if session_id not in store: # 세션이 없다면 새로 생성
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id] # 이미 저장된 상태(해당 세션의 메모리를 반환)

# 6. RunnablewithMessageHistory 적용
with_message_history = RunnableWithMessageHistory(
    model, # 실행할 모델
    get_session_history, # 세션별 history 반환함수 (세션값을 꺼내올 함수이름지정)
)

# 7. 실행요청 목록 정의
requests = [
    {"session_id":"abc2", "message":"안녕? 난 홍진모야."},
    {"session_id":"abc2", "message":"내 이름이 뭐지?"},
    {"session_id":"abc3", "message":"내 이름이 뭐지?"},
    {"session_id":"abc2", "message":"아까 우리가 무슨 얘기 했지?"}
]

# 8. 일반 invoke 실행 (for문 사용)
# memory -> RAG -> Agent -> Langraph -> fastAPI -> Mini-Project
print("\n === 일반 invoke 실행 ===\n")

for req in requests:
    # 세션ID 설정
    # configurable => 랭체인 내부적으로 이 설정은 실행시점에 동적으로 바뀔수 있다라고 지정해주는 옵션(예약어)
    # session_id => 누가 대화하고 있는지를 구분하는 방번호
    # req["session_id"] => 사용자로부터 들어온 요청(requests)에서 실제 세션ID값을 추출하여 할당.
    config = {"configurable":{"session_id":req["session_id"]}} #req['abc2']
    
    # 모델 실행
    response = with_message_history.invoke(
        [HumanMessage(content=req["message"])], # 세션별 대화내용 전달
        config=config # 세션 id값을 전달
    ) # 새롭게 입력을 받을때마다 전의 저장된 데이터 같이 전달
    
    # 세션정보와 함께 출력
    print(f"[Session: {req['session_id']}]") # 세션id
    print(f"User: {req['message']}") # 사용자대화
    print(f"AI: {response.content}") # 모델에서 보내준 내용출력 response -> 문자열+기타내용 
    print("="*80)

# for문 밖
# 9. stream 실행예시
print("\n== stream 실행(abc2 유지)===\n")

stream_config = {"configurable":{"session_id":"abc2"}}
print("[Session: abc2]")
print("User: 내가 어느나라 사람인지 맞춰보고, 그나라의 문화에 대해서 말해보세요")
print("AI: ",end="",flush=True)

# 스트리밍 방식으로 모델 응답출력(한글자씩 실시간으로 응답을 받아서 출력)
for chunk in with_message_history.stream(
    [HumanMessage(content="내가 어느나라 사람인지 맞춰보고, 그나라의 문화에 대해서 말해보세요")], # 세션별 대화내용 전달
        config=stream_config
):
    print(chunk.content, end="", flush=True) # 각 응답 조각을 즉시 출력(채팅처럼)

print("\n"+"="*80)

# 10. 현재 세션 메모리의 상태 확인
print("\n === 현재 세션 메모리 상태 === \n")

for session_id, history in store.items(): # {키:값~}
    print(f"[Session: {session_id}]")
    for msg in history.messages:
        print(f" - {msg.type} : {msg.content}") # 메세지 타입(human/ai)과 내용 출력 
    print("="*80)  