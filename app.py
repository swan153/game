import random
import time
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="두더지 잡기 게임", page_icon="🔨", layout="centered")

# 초기 세션 상태 설정
if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "target_index" not in st.session_state:
    st.session_state.target_index = None
if "game_active" not in st.session_state:
    st.session_state.game_active = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0

GAME_DURATION = 30  # 게임 시간 (초)
GRID_SIZE = 9        # 3x3 격자


def start_game():
    st.session_state.score = 0
    st.session_state.game_active = True
    st.session_state.game_over = False
    st.session_state.start_time = time.time()
    st.session_state.target_index = random.randint(0, GRID_SIZE - 1)


def whack(index):
    if st.session_state.game_active and index == st.session_state.target_index:
        st.session_state.score += 10
        # 두더지 위치 변경 (이전 위치와 다르게)
        new_target = random.randint(0, GRID_SIZE - 1)
        while new_target == st.session_state.target_index:
            new_target = random.randint(0, GRID_SIZE - 1)
        st.session_state.target_index = new_target


# 헤더 영역
st.title("🔨 Streamlit 두더지 잡기!")
st.write("30초 동안 나타나는 두더지(🐹)를 클릭해서 높은 점수를 얻으세요!")

# 최고 점수 및 현재 점수 표시
col_score1, col_score2, col_score3 = st.columns(3)
col_score1.metric("최고 점수", f"{st.session_state.high_score}점")
col_score2.metric("현재 점수", f"{st.session_state.score}점")

# 남은 시간 계산 및 게임 종료 처리
if st.session_state.game_active:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, GAME_DURATION - int(elapsed_time))
    col_score3.metric("남은 시간", f"{remaining_time}초")

    if remaining_time <= 0:
        st.session_state.game_active = False
        st.session_state.game_over = True
        st.session_state.target_index = None
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
        st.rerun()
else:
    col_score3.metric("남은 시간", f"{GAME_DURATION}초")

# 시작/재시작 버튼
if not st.session_state.game_active:
    if st.button("🚀 게임 시작", on_click=start_game, type="primary", use_container_width=True):
        st.rerun()

if st.session_state.game_over:
    st.success(f"🎉 게임 종료! 최종 점수: {st.session_state.score}점")

st.divider()

# 3x3 게임 격자 출력
cols = st.columns(3)
for i in range(GRID_SIZE):
    col = cols[i % 3]
    with col:
        if st.session_state.game_active and i == st.session_state.target_index:
            label = "🐹"  # 두더지 등장
            button_type = "primary"
        else:
            label = "🕳️"  # 굴 (빈자리)
            button_type = "secondary"

        st.button(
            label,
            key=f"hole_{i}",
            on_click=whack,
            args=(i,),
            disabled=not st.session_state.game_active,
            use_container_width=True,
        )

# 커스텀 스타일 적용 (버튼 크기 조절)
st.markdown(
    """
    <style>
    div[data-testid="stButton"] > button {
        height: 100px;
        font-size: 2.5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
