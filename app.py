import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import time
import os

# --- [비밀 금고 자동 생성기] ---
# 네가 터미널을 어디서 켰든 상관없이, 알아서 폴더랑 파일을 만들고 시작함!
try:
    os.makedirs(".streamlit", exist_ok=True)
    with open(".streamlit/secrets.toml", "w", encoding="utf-8") as f:
        f.write("""
[connections.gsheets]
type = "service_account"
project_id = "logical-matrix-494213-d5"
private_key_id = "eaa6db244b4d00db67a3b720debdb16cc220ebf8"
private_key = \"\"\"-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDDOWlUFKco+dy6
y89h4Q8OuEEAHmI0Z69LsFNF7/yg3lasklwQXtuDugKx2ZSPQg213UJZWe+JOvpB
c1SROABpYNamvTY9flxqiGDoH25kZeiejMweEXPChZD+Rb88KMxnDE/YzhEBwXLH
ofr7Zy+UwqTp8LijRN1dMcaw5bzx5piUb6XIcRe0Q8m3mkmRzr0tMVLRzwqQVNgQ
ZAKokHvnaIJlAhWSkdK5v4tuehHwH0opfLezLTFSvHmrQkjfHIEqkPTAY70I2y8E
nMD3+2AYFS34BL+daQYGvmBCEfri4DlYBDAzVmYa0phD+0tly+yg1mLvor4DdrhF
fk7cFi//AgMBAAECggEAYIHJkVCSX/3AwbDOCH9Wz7qDG3lpp6lX7U0xpUGhO68d
3rqNe2RBFOnHuj6qo3UOTQifa4c7lDXND7zhIday0WUXR58CqLyGF/3qFeWvzz7X
k0VcBEMxXAhmKGS3SBiNDyX1dOJNYvZL9OccqNoWGe5s0t72j3OUEKVyKPGxCU1L
xQ/WsETExS0oLkvzOEdoVfqJCIwuY0QnwCMGNQLDmOsX7Gz2lIhdCTvBctHFfzxe
BLHhtS880AzqEuBIIbcA2NbhL7CeLmuQxglkqqNzuFZCi1QJZ2xJfdFS5q3Sa02R
NZ58udxHYZxlS1ZFWDdCTg52pRWw0LtdWCfh93XNFQKBgQD/V1wawMuDVn2OJL6N
zpZKgdtH82kSTe3swD0MqhX56acdeu2FsY/pce5m/40EbCWG7ESz6BvKg5GBOM8+
/oi7/o/Ak7Aza4cMs4CpGtVrC6DoeLXWVggPE0b5CUoBLHDL4/twDk6muWkXlLUZ
bPZR2ir90Sf5RCukIblWXULobQKBgQDDuljtXQ/nCzJa0mZlFuJcQbCAr0EUnJLW
ZwqqZ5zhRCrSZO9lSbwpP8hNe5hIg7xW8J5+nnVjOjlk8u44akoc2BbayteseCP/
mWoMGQcK2PlMyj2k1Vd/uSX4EgtnsYdAYzeuS6uVH1Cg3/wPBK+0ByFxaPWuubSL
QoaKi+OOmwKBgE+8Bu3vwF1d980YWkzL8xCHJmN8dhYaMa7ZhPbccgpdVSsWhO9X
uDnMswaEzJNR9hIA259WXr9JgHlatRTVxPr3jgoz1DTqYfysXQPxdi18Lx4I+7dX
nCKhAWuo4+wj5YE1ywF95j+X7GJJtJeg9/Yta3lhA9uJ1xrk0QxQCSGtAoGAai4Q
igw/UUbItW6Ir/R/Li9Qsi7g7m6WVgumRJVbDPWvCV5KZLdghTwdzLLtBQG6TavR
P710zzTJ6BLF2wMGW6l6lI0P/XdbiBDQ7+kv4dmdPORGFsLJ6fcmOvKHD2TGi86H
aV2Rop9PXUbFddxD+TUZFm4rQfNql1WqqUSEWVsCgYBIeUxJfJjLtRTWo/kfxFdd
qKsCctBna4UcSuXB5bDTNTWx4euVcGqILFu1sm2RLJpAU1/wNTJG36q/y83XK5Is
NrPIJkPFo9Z5POru8p53P3B/rBJKJeQViGZndNUOaJFZ9720LRToFgFBwNInHt6M
AYWOApW9c7I/PGwYvdiUog==
-----END PRIVATE KEY-----
\"\"\"
client_email = "cozybois@logical-matrix-494213-d5.iam.gserviceaccount.com"
client_id = "104273753685531476665"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/cozybois%40logical-matrix-494213-d5.iam.gserviceaccount.com"
spreadsheet = "https://docs.google.com/spreadsheets/d/1bGoA_Yrm_R7eZL4yqjW9ASFTJg61MNV81vPeAQFBjs8/edit?usp=sharing"
        """)
except Exception as e:
    pass
# --------------------------------

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="For Cozybois", page_icon="🛋️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #e0e0e0; }
    .stButton>button { width: 100%; background-color: #da291c; color: white; border-radius: 8px; height: 3.5em; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ff3c2e; transform: scale(1.02); color: white; }
    .stTextArea textarea, .stTextInput input { background-color: #252525 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 아주 깨-끗해진 연결 코드 (위에 만든 금고에서 알아서 읽어옴!)
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(sheet_name, columns):
    try:
        return conn.read(worksheet=sheet_name, ttl=10)
    except:
        return pd.DataFrame(columns=columns)

# 3. 사이드바 (마스터 컨트롤)
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

# 4. 데이터 실시간 로드
df_veto = load_data("vetoes", ["name", "veto"])
df_options = load_data("options", ["item"])
df_members = load_data("members", ["name"])

# ⭐ 빈 시트의 오지랖(숫자 인식) 방지 및 문자열(텍스트) 강제 지정
df_options["item"] = df_options["item"].astype(str).replace(["nan", "None", "<NA>"], "")
df_members["name"] = df_members["name"].astype(str).replace(["nan", "None", "<NA>"], "")

# 리스트 변환 (빈칸 제외하고 깔끔하게)
options = [x for x in df_options["item"].tolist() if x.strip()] if not df_options.empty else ["강남역", "홍대"]
friends = [x for x in df_members["name"].tolist() if x.strip()] if not df_members.empty else ["성우", "창민"]
# 5. 메인 화면
st.title("🛋️ For Cozybois")
st.markdown("##### 실시간 편집 & 공유 시스템")
# --- [새로 추가할 부분: 카톡 초대장 복사] ---
with st.expander("💌 카톡 초대장 복사하기"):
    st.markdown("아래 박스 오른쪽 위에 있는 **복사 아이콘(📋)**을 눌러서 단톡방에 뿌려!")
    
    # 앱 주소는 나중에 Streamlit 배포 주소로 바꿔줘!
    APP_URL = "https://your-app-name.streamlit.app" 
    
    invite_text = f"""🛋️ [For Cozybois] 오늘 어디 갈래?

✔️ "아무거나" 금지! 가기 싫은 곳 딱 하나만 밴(Ban) 해라.
✔️ 마지막 결정은 운명의 주사위가 한다 🎲

👇 지금 바로 접속해서 내 밴 등록하기 👇
{APP_URL}
"""
    st.code(invite_text, language="text")
# ------------------------------------
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
            <div style="background-color:#da291c; padding:30px; border-radius:15px; text-align:center;">
                <h3 style="color:white; margin:0; opacity:0.8;">Today's Choice</h3>
                <h1 style="color:white; font-size:40px; margin-top:10px;">✨ {final} ✨</h1>
            </div>
        """, unsafe_allow_html=True)
        
        share_text = f"🛋️ For Cozybois 모임 결정!\n\n✨ 오늘의 장소: {final}\n\n결과 확인하기:\nhttps://docs.google.com/spreadsheets/d/1bGoA_Yrm_R7eZL4yqjW9ASFTJg61MNV81vPeAQFBjs8" 
        
        st.write(" ")
        st.info("📋 아래 내용을 복사해서 카톡에 뿌리세요:")
        st.code(share_text)
