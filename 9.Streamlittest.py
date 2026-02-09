from callfunction import *
import streamlit as st

# API키 불러오기
api_key = st.secrets["OPENAI_API_KEY"] # secrets.toml 파일에서 불러오기

# LLM 초기화
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

prompt = PromptTemplate.from_template(" '{topic}' 주제에 대해서 한 문장으로 설명해줘")
chain = prompt | llm | StrOutputParser() #익명객체

# --- Streamli UI 구성 ---
## 1. page_title(브라우저 탭 제목) page_icon(브라우저탭 아이콘) layout=화면중앙정렬
st.set_page_config(page_title="LangChain Chat", page_icon="☆", layout="centered")

##. md파일(### h3)
st.markdown("### ☆ LangChain + Streamlit 대화형 예제")

# 2. 세션 상태 초기화 => st.session_state (항목 초기화)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# -- 입력 처리 함수 정의 -- 
def process_input():
    user_text = st.session_state["input_box"].strip()
    if user_text:
        st.session_state["messages"].append(("user",user_text)) # humanmessage, 사용자가 한말
        # 생성중입니다.
        with st.spinner("♠♠♠ 답변을 생성하고 있습니다... ♠♠♠"):
            result = chain.invoke({"topic":user_text})
        st.session_state["messages"].append(("ai",result)) # AI 응답저장
              
# -- 입력창과 버튼 UI 구성 -- 
col1, col2 = st.columns([5,1]) # 두개의 컬럼생성(비율 5:1)

with col1:
    st.text_input("Topic", placeholder="주제를 입력하세요...", key="input_box") # 세션id 역할
      
with col2:
    st.write("") # 버튼을 입력창과 같은 높이에 맞추기위해 빈줄 추가
    st.write("")
    submit = st.button("질문하기", on_click=process_input) #1. 버튼의 이름 2. on_click="호출할 함수명(괄호는 X)"

# 말풍선(대화 기록 출력) UI 구성
for role, text in st.session_state["messages"]: # 저장된 문자열(user, ai 구분해서 출력)
    if role == "user": # 사용자 메세지 오른쪽배치
        st.markdown(
            f"""
            <div style='text-align:right; margin:10px;'>
                <div style='display:inline-block;
                            background:#DCF8C6; padding:12px;
                            border-radius:15px; max-width:70%;
                            color:black;'>
                    <b style='color:#075E54;'> 😊사용자 </b><br> {text}
                </div>
            </div>
            """,            
            unsafe_allow_html= True # streamlit에서 HTML태그를 그대로 랜더링(출력) rendering
        )
    else: # AI 메세지 출력
        st.markdown(
            f"""
            <div style='text-align:left; margin:10px;'>
                <div style='display:inline-block;
                            background:#E6E6E6; padding:12px;
                            border-radius:15px; max-width:70%;
                            color:black;'>
                    <b style='color:#333;'> 🤖AI </b><br> {text}
                </div>
            </div>
            """,            
            unsafe_allow_html= True
        )