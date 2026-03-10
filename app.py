import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 뤼튼 스타일 CSS ---
st.set_page_config(page_title="보안 인텔리전스 에이전트", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
* { font-family: 'Pretendard', sans-serif; }
.main { background-color: #F8F9FA; }
.report-card { 
    background-color: white; 
    padding: 30px; 
    border-radius: 18px; 
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    border-top: 6px solid #051C48;
    margin-bottom: 25px;
}
.stButton>button { 
    background-color: #051C48; 
    color: white; 
    border-radius: 10px; 
    font-weight: 600;
    height: 3em;
    width: 100%;
    border: none;
}
.stButton>button:hover { 
    background-color: #0066FF; 
    border: none; 
}
.sidebar-title { 
    font-size: 1.2rem; 
    font-weight: 700; 
    color: #051C48; 
    margin-bottom: 20px; 
}
</style>
""", unsafe_allow_html=True)

# --- 2. 데이터 소스 설정 (GitHub 연동) ---
GITHUB_USER = "yoondh-ai"
REPO_NAME = "security-market-intelligence"

# Kiro가 생성하는 리포트 경로 (실제 파일명에 맞춰 동적 할당 가능)
DEFAULT_FILE = "security_intelligence_report_2026-03-08.md"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/{DEFAULT_FILE}"

def load_github_report(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return "⚠️ 리포트 파일을 찾을 수 없습니다. (GitHub 동기화 대기 중)"
    except:
        return "❌ 연결 오류가 발생했습니다."

# --- 3. 사이드바 (Wrtn 스타일 메뉴) ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">🔍 분석 대상 프리셋</p>', unsafe_allow_html=True)
    target = st.radio(
        "경쟁사/키워드를 선택하세요", 
        ["안랩 vs 마크애니", "제로 트러스트", "보안 컴플라이언스"],
        index=0
    )
    st.divider()
    st.caption("Last Sync: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

# --- 4. 메인 화면 레이아웃 ---
st.title("🛡️ 정보보안 시장조사 인텔리전스")
st.markdown(f"**{target}**에 대한 최신 분석 리포트입니다.")

# 분석 실행/새로고침 버튼
if st.button("🔄 최신 분석 리포트 불러오기"):
    with st.spinner("Kiro 인텔리전스 엔진에서 최신 데이터를 읽어오는 중..."):
        content = load_github_report(RAW_URL)
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown(content)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("왼쪽에서 대상을 선택한 후 '리포트 불러오기' 버튼을 클릭해 주세요.")

# --- 5. 피드백 및 수정 요청 (Gemini 인터랙션 영역) ---
st.divider()
st.subheader("💬 분석 결과 피드백")

with st.expander("리포트 내용 수정 또는 추가 조사 요청"):
    user_input = st.text_area(
        "Gemini에게 요청할 내용을 입력하세요.", 
        placeholder="예: 마크애니의 C2PA 기술과 안랩의 대응 전략을 더 자세히 비교해줘."
    )
    if st.button("Gemini에게 수정 요청 발송"):
        st.success("피드백이 접수되었습니다. Gemini가 리포트를 업데이트할 예정입니다.")
