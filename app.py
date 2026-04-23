import streamlit as st
import random
import time

st.set_page_config(page_title="독재자의 칙령", page_icon="👑")

st.title("👑 독재자의 칙령 v1.2")
st.info("아무거나라고 말한 죄, 독재자가 심판한다.")

# 사이드바: 독재자 전용 설정
with st.sidebar:
    st.header("🕵️ 독재자 비밀 설정")
    master_pick = st.text_input("내가 가고 싶은 장소 (이름 똑같이 적기)", "")
    bias_power = st.slider("내 장소 당첨 확률 보정 (%)", 0, 100, 50)
    
    st.write("---")
    options_str = st.text_area("후보지들 (쉼표 구분)", "강남역 삼겹살, 홍대 파스타, 이태원 타코")
    options = [opt.strip() for opt in options_str.split(",") if opt.strip()]

# 메인 화면: 친구들 입력
friends_str = st.text_input("오늘 모이는 친구들", "성우, 창민, 친구1")
friends = [f.strip() for f in friends_str.split(",") if f.strip()]

st.subheader("🚫 거부권 행사")
vetoes = {}
cols = st.columns(len(friends))
for i, friend in enumerate(friends):
    with cols[i]:
        vetoes[friend] = st.selectbox(f"{friend}의 밴", ["없음"] + options, key=f"v_{friend}")

# 결과 도출 로직
if st.button("🔥 칙령 선포"):
    with st.spinner("운명을 결정하는 중..."):
        time.sleep(1.5) # 긴장감 조성용 딜레이
        
        forbidden = set(vetoes.values())
        remaining = [opt for opt in options if opt not in forbidden]
        
        if not remaining:
            st.error("모두 거부당했습니다! 다시 정하세요.")
        else:
            # 확률 조작 로직 (마스터 픽이 남은 리스트에 있다면 확률 업)
            if master_pick in remaining:
                # master_pick을 리스트에 여러 개 넣어서 뽑힐 확률을 높임
                weights = [bias_power if opt == master_pick else 10 for opt in remaining]
                final = random.choices(remaining, weights=weights, k=1)[0]
            else:
                final = random.choice(remaining)
                
            st.balloons()
            st.success(f"🎊 오늘의 칙령: **[{final}]**")
            
            # 벌칙 기능 추가
            st.divider()
            st.subheader("💀 오늘의 독박 (랜덤)")
            victim = random.choice(friends)
            st.warning(f"예약 및 장소 안내는 **[{victim}]** 가(이) 담당한다. 토 달지 마라.")