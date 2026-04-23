import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time
import os

# --- [비밀 금고 자동 생성기] ---
# 서버에서도 로컬처럼 안정적으로 돌아가도록 금고를 확인하는 로직
try:
    os.makedirs(".streamlit", exist_ok=True)
    if not os.path.exists(".streamlit/secrets.toml"):
        with open(".streamlit/secrets.toml", "w", encoding="utf-8") as f:
            f.write("# Secrets are managed in Streamlit Cloud Settings")
except:
    pass

# 1. 페이지 설정 및 디자인 (Man Utd Red 테마)
st.set_page_config(page_title="For Cozybois", page_icon="🛋️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #e0e0e0; }
    .stButton>button {
        width: 100%; background-color: #da291c; color: white;
        border-radius: 8px; height: 3.5em; font-weight: bold; border: none;
    }
    .stButton>button:hover { background-color: #ff3c2e; transform: scale(1.02); color: white; }
    .stTextArea textarea, .stTextInput input { background-color: #252525 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(sheet_name, columns):
    try:
        # API 할당량 보호를 위해 5초 캐시 적용
        return conn.read(worksheet=sheet_name, ttl=5)
    except:
        return pd.DataFrame(columns=columns)

# 3. 사이드바: 마스터 컨트롤 (GGMU 전용)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg", width=80)
    st.header("⚙️ Admin Control")
    admin_key = st.text_input("Admin Access", type="password")
    
    master_pick = ""
    bias = 0
    if admin_key == "GGMU":
        st.success("✅ Admin Verified")
        master_pick = st.text_input("🤫 내 마음속 1순위", "")
        bias = st.slider("당첨 확률 보정 (%)", 0, 100, 80)
        if st.button("🔴 모든 데이터 초기화"):
            conn.update(worksheet="vetoes", data=pd.DataFrame(columns=["name", "veto"]))
            st.rerun()

# 4. 데이터 로드 및 전처리
df_veto = load_data("vetoes", ["name", "veto"])
df_options = load_data("options", ["item"])
df_members = load_data("members", ["name"])

df_options["item"] = df_options["item"].astype(str).replace(["nan", "None", "<NA>"], "")
df_members["name"] = df_members["name"].astype(str).replace(["nan", "None", "<NA>"], "")

options = [x for x in df_options["item"].tolist() if x.strip()] if not df_options.empty else ["강남역", "홍대"]
friends = [x for x in df_members["name"].tolist() if x.strip()] if not df_members.empty else ["성우", "창민"]

# 5. 메인 화면
st.title("🛋️ For Cozybois")
st.markdown("##### 실시간 편집 & 공유 시스템")

# --- [A] 카톡 초대장 섹션 (진짜 주소 반영) ---
with st.expander("💌 카톡 초대장 복사하기"):
    st.markdown("오른쪽 상단 **복사 아이콘(📋)**을 눌러서 단톡방에 뿌려!")
    
    # 성우의 진짜 앱 주소로 업데이트 완료!
    REAL_APP_URL = "https://for-the-lazyss.streamlit.app"
    
    invite_text = f"""🛋️ [For Cozybois] 오늘 어디 갈래?

✔️ "아무거나" 금지! 가기 싫은 곳 딱 하나만 밴(Ban) 해라.
✔️ 마지막 결정은 운명의 주사위가 한다 🎲

👇 지금 바로 접속해서 내 밴 등록하기 👇
{REAL_APP_URL}
"""
    st.code(invite_text, language="text")

# --- [B] 실시간 편집 섹션 ---
with st.expander("📝 멤버 및 장소 후보 편집하기"):
    col_edit1, col_edit2 = st.columns(2)
    with col_edit1:
        st.write("👥 멤버 편집")
        edited_members = st.data_editor(df_members, num_rows="dynamic", use_container_width=True, key="edit_members")
    with col_edit2:
        st.write("📍 장소 편집")
        edited_options = st.data_editor(df_options, num_rows="dynamic", use_container_width=True, key="edit_options")
    
    if st.button("✅ 변경사항 저장하기"):
        conn.update(worksheet="members", data=edited_members)
        conn.update(worksheet="options", data=edited_options)
        st.success("시트에 저장되었습니다!")
        st.rerun()

st.write("---")

# --- [C] 밴 현황 및 입력 ---
st.write("### 📊 실시간 밴 현황")
if not df_veto.empty:
    st.table(df_veto)

st.subheader("🚫 거부권 행사")
c1, c2 = st.columns(2)
with c1:
    my_name = st.selectbox("누구야?", friends)
with c2:
    my_veto = st.selectbox("여긴 진짜 가기 싫다", ["없음"] + options)

if st.button("밴 등록하기"):
    new_entry = pd.DataFrame([{"name": my_name, "veto": my_veto}])
    updated_veto = pd.concat([df_veto, new_entry], ignore_index=True).drop_duplicates(subset=["name"], keep="last")
    conn.update(worksheet="vetoes", data=updated_veto)
    st.success("반영 완료!")
    st.rerun()

st.write("---")

# --- [D] 결과 도출 ---
if st.button("🚀 Roll the Dice"):
    forbidden = set(df_veto["veto"].tolist())
    remaining = [opt for opt in options if opt not in forbidden and opt != "없음"]

    if not remaining:
        st.error("남은 장소가 없습니다. 밴을 좀 풀어보세요.")
    else:
        with st.spinner("운명 계산 중..."):
            time.sleep(1)
        
        if master_pick in remaining:
            weights = [bias if opt == master_pick else (100-bias)/(len(remaining)-1) for opt in remaining]
            final = random.choices(remaining, weights=weights, k=1)[0]
        else:
            final = random.choice(remaining)
            
        st.balloons()
        st.markdown(f"""
            <div style="background-color:#da291c; padding:30px; border-radius:15px; text-align:center; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <h3
