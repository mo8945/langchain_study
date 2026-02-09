from callfunction import *
# 추가 (X) -> MessagesPlaceholder=>ChatMessageHistory
# 대화를 기록 관리해주는 Class
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import OpenAI

# 1. LLM 초기화
llm = OpenAI(temperature=0.5)

# 대화 기록 객체 생성
history = ChatMessageHistory()

# 기능 => 함수(=직원)

# 1. 매개변수 X    반환값 X => 단순, 반복적인 일
# 2. 매개변수 O    반환값 X => 데이터 저장목적, 게산 목적(재정=>금액)
# 3. 매개변수 O    반환값 O => 계산목적(=보고)
def show_history(): # work function() => 협업 => 함수들이 순서에따라서 호출 => 실행
    # 현재까지의 대화기록을 보기 좋게 출력
    print("\n==대화기록==")
    # for 출력변수 in 출력대상자(=객체)
    for msg in history.messages:
        # 구분
        role = "사용자" if msg.type == "human" else "AI"
        print(f"{role}: {msg.content}")
    print("========================================\n")

def main(): 
    print("대화를 시작합니다. 'exit' 입력시 종료합니다.")
    while True:
        user_input = input(">>>")
        if user_input.lower() == 'exit':
            print("프로그램을 종료합니다.")
            break
        # 사용자 메시지 기록
        history.add_user_message(user_input)
        # LLM 응답 생성
        ai_response = llm.invoke(user_input)
        # AI 메시지 기록
        history.add_ai_message(ai_response)
        # 응답출력
        print(f"AI: {ai_response}")
        # 대화 기록 출력
        show_history()

# 함수가 없는 경우  => 그냥 실행 OK
# 함수가 있는 경우  => 모듈형태로 많이 사용된다.
# 1. => 현재파일에서 실행시키는 경우
# 2. => 외부에서 모듈로 사용하는 경우
if __name__ == "__main__":
    main()
    print('__name__=>',__name__)