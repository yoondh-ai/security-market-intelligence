import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient  # Tavily 사용 예시

# --- 1. API 키 설정 (Streamlit Secrets 사용 권장) ---
# st.secrets에 등록된 키를 불러옵니다.
GENAI_API_KEY = st.secrets["GEMINI_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

genai.configure(api_key=GENAI_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# --- 2. 에이전트 핵심 함수 ---
def run_workflow(keyword, period, my_info):
    # Step 1: 뉴스 수집 (Tavily AI 검색)
    search_result = tavily.search(
        query=f"{keyword} 보안 뉴스 {period}", 
        search_depth="advanced", 
        max_results=10
    )
    
    # Step 2 & 3: Gemini 분석 및 리포트 생성
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""당신은 정보보안 분석가입니다. 다음 뉴스 데이터를 바탕으로 리포트를 작성하세요.

키워드: {keyword}
자사정보: {my_info}
데이터: {search_result}

[필수 포함 내용]
1. 뉴스별 핵심 요약 및 발행일
2. 타 경쟁사와의 기술적 차별점 분석
3. 자사 솔루션과의 비교 및 전략적 제언

(마크다운 형식으로 작성할 것)"""
    
    response = model.generate_content(prompt)
    return response.text

# --- 3. UI 부분 ---
st.title("🛡️ 실시간 보안 인텔리전스 에이전트 (API 연동형)")

with st.sidebar:
    keyword = st.text_input("키워드")
    my_info = st.text_area("자사 정보")
    
    if st.button("🚀 실시간 분석 시작"):
        with st.spinner("뉴스를 수집하고 Gemini가 분석 중입니다..."):
            report = run_workflow(keyword, "2026", my_info)
            st.session_state['latest_report'] = report

if 'latest_report' in st.session_state:
    st.markdown(st.session_state['latest_report'])
