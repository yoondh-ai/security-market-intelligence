import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

# --- 1. API 키 설정 (Streamlit Secrets 사용 권장) ---
try:
    GENAI_API_KEY = st.secrets["GEMINI_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception as e:
    st.error(f"API 키 로드 실패: {e}")
    st.stop()

genai.configure(api_key=GENAI_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# --- 2. 에이전트 핵심 함수 ---
def run_workflow(keyword, period, my_info):
    try:
        # Step 1: 뉴스 수집 (Tavily AI 검색)
        search_result = tavily.search(
            query=f"{keyword} 보안 뉴스 {period}", 
            search_depth="advanced", 
            max_results=10
        )
        
        # Step 2 & 3: Gemini 분석 및 리포트 생성
        # 2026년 실제 사용 가능한 모델들 (API 키 테스트로 확인됨)
        model_configs = [
            ('models/gemini-2.5-flash', {}),  # 최신 고속 모델
            ('models/gemini-2.5-pro', {}),    # 최신 고성능 모델
            ('models/gemini-2.0-flash', {}),  # 안정 버전
            ('models/gemini-flash-latest', {}),  # 최신 플래시
            ('models/gemini-pro-latest', {}),    # 최신 프로
        ]
        
        last_error = None
        for model_name, config in model_configs:
            try:
                model = genai.GenerativeModel(model_name)
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
            except Exception as model_error:
                last_error = str(model_error)
                continue
        
        # 모든 모델 실패 시
        raise Exception(f"모든 모델 시도 실패. 마지막 오류: {last_error}")
                
    except Exception as e:
        error_msg = str(e)
        return f"""❌ 오류 발생: {error_msg}

**해결 방법:**
1. 먼저 상단의 '🔍 API 키 테스트' 버튼을 클릭하여 사용 가능한 모델을 확인하세요
2. API 키가 올바른지 확인: https://aistudio.google.com/app/apikey
3. 새 API 키를 생성하여 Streamlit Secrets에 업데이트하세요

**현재 시도한 모델들:**
- models/gemini-2.5-flash (최신 고속)
- models/gemini-2.5-pro (최신 고성능)
- models/gemini-2.0-flash (안정 버전)
- models/gemini-flash-latest
- models/gemini-pro-latest
"""

# --- 3. UI 부분 ---
st.title("🛡️ 실시간 보안 인텔리전스 에이전트 (API 연동형)")

# API 키 테스트 버튼 추가
if st.button("🔍 API 키 테스트"):
    try:
        # 사용 가능한 모델 목록 확인
        models = genai.list_models()
        st.success("✅ Gemini API 연결 성공!")
        st.write("사용 가능한 모델:")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                st.write(f"- {model.name}")
    except Exception as e:
        st.error(f"❌ API 키 오류: {str(e)}")
        st.info("해결 방법: https://aistudio.google.com/app/apikey 에서 새 API 키를 생성하세요")

st.divider()

with st.sidebar:
    keyword = st.text_input("키워드", placeholder="예: 안랩")
    my_info = st.text_area("자사 정보", placeholder="예: 마크애니 - DRM 및 워터마킹 전문")
    
    if st.button("🚀 실시간 분석 시작"):
        if not keyword:
            st.error("키워드를 입력해주세요")
        else:
            with st.spinner("뉴스를 수집하고 Gemini가 분석 중입니다..."):
                report = run_workflow(keyword, "2026", my_info)
                st.session_state['latest_report'] = report

if 'latest_report' in st.session_state:
    st.markdown(st.session_state['latest_report'])
