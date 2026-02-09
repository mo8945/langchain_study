from callfunction import *

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
prompt = ChatPromptTemplate.from_template("{input}")
chain = prompt | llm | StrOutputParser()

#사용자 선택에 따라 사용할 프롬프트 템플릿 정의
prompt_map = {
    "1" : ("요약","다음 내용을 한문장으로 요약해 주세요\n 내용:{text}"),
    "2" : ("키워드","다음 내용에서 핵심 키워드 5개만 뽑아주세요\n 내용:{text}"),
    "3" : ("답변","다음 내용에 3문장 이내로 답변해 주세요\n 내용:{text}")
}

print("1) 요약")
print("2) 키워드")
print("3) 3문장 내로답변")

sel = input("선택(1~3): ").strip()
#잘못선택
if sel not in prompt_map:
    raise Sys