import random
import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 페이지 기본 설정
st.set_page_config(
    page_title="말랑말랑 두더지 잡기 🔨", page_icon="🐹", layout="centered"
)

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "moles" not in st.session_state:
    st.session_state.moles = []  # 현재 두더지가 있는 위치 배열 (2개)
if "last_move_time" not in st.session_state:
    st.session_state.last_move_time = 0
if "game_active" not in st.session_state:
    st.session_state.game_active = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0

GAME_DURATION = 30  # 게임 시간 (30초)
GRID_SIZE = 9  # 3x3 격자

# 난이도 설정 (두더지가 유지되는 시간 단위: 초)
DIFFICULTY_SETTINGS = {
    "🌱 쉬움 (1.5초)": 1.5,
    "⚡ 보통 (1.0초)": 1.0,
    "🔥 어려움 (0.6초)": 0.6,
}


def spawn_moles():
    """두더지 2마리를 중복되지 않는 랜덤한 구멍에 배치"""
    st.session_state.moles = random.sample(range(GRID_SIZE), 2)
    st.session_state.last_move_time = time.time()


def start_game():
    st.session_state.score = 0
    st.session_state.game_active = True
    st.session_state.game_over = False
    st.session_state.start_time = time.time()
    spawn_moles()


def whack(index):
    """두더지를 잡았을 때 호출"""
    if st.session_state.game_active and index in st.session_state.moles:
        st.session_state.score += 10
        # 잡힌 두더지만 새로운 곳으로 이동
        st.session_state.moles.remove(index)
        available_holes = [
            i for i in range(GRID_SIZE) if i not in st.session_state.moles
        ]
        st.session_state.moles.append(random.choice(available_holes))
        st.session_state.last_move_time = time.time()


# --- CSS 스타일 적용 (파스텔톤 / 동글동글한 예쁜 UI) ---
st.markdown(
    """
    <style>
    /* 전체 배경 및 폰트 감성 적용 */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* 두더지 버튼 스타일링 */
    div[data-testid="stButton"] > button {
        height: 110px;
        font-size: 3rem !important;
        border-radius: 20px !important;
        border: 2px solid #e2e8f0 !important;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.15s ease-in-out !important;
        background-color: #ffffff !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.12) !important;
    }
    
    div[data-testid="stButton"] > button:active {
        transform: translateY(2px) scale(0.98);
    }

    /* 카드 형태 대시보드 */
    .stat-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 헤더
st.title("🔨 말랑말랑 두더지 잡기!")
st.caption("두 마리씩 튀어나오는 두더지를 30초 동안 잡아보세요!")

# 사이드바 또는 상단 난이도 선택
difficulty_name = st.selectbox(
    "🎯 난이도 선택",
    options=list(DIFFICULTY_SETTINGS.keys()),
    disabled=st.session_state.game_active,
)
mole_timeout = DIFFICULTY_SETTINGS[difficulty_name]

# 게임 진행 중일 때 화면을 주기에 맞춰 자동 갱신 (0.1초마다 체크)
if st.session_state.game_active:
    st_autorefresh(interval=100, key="mole_refresh")

    # 두더지 자동 이동 체크 (지정된 시간 동안 안 누르면 재배치)
    if time.time() - st.session_state.last_move_time >= mole_timeout:
        spawn_moles()
        st.rerun()

# 남은 시간 계산
if st.session_state.game_active:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, GAME_DURATION - int(elapsed_time))

    if remaining_time <= 0:
        st.session_state.game_active = False
        st.session_state.game_over = True
        st.session_state.moles = []
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
        st.rerun()
else:
    remaining_time = GAME_DURATION

# 대시보드 (점수판)
col1, col2, col3 = st.columns(3)
col1.metric("🏆 최고 점수", f"{st.session_state.high_score}점")
col2.metric("⭐ 현재 점수", f"{st.session_state.score}점")
col3.metric("⏱️ 남은 시간", f"{remaining_time}초")

st.write("")

# 시작 / 게임 오버 안내
if not st.session_state.game_active:
    if st.button(
        "🚀 게임 시작하기",
        on_click=start_game,
        type="primary",
        use_container_width=True,
    ):
        st.rerun()

if st.session_state.game_over:
    st.balloons()
    st.success(
        f"🎉 시간 종료! 최종 점수는 **{st.session_state.score}점**입니다!"
    )

st.divider()

# 3x3 격자 출력
cols = st.columns(3)
for i in range(GRID_SIZE):
    col = cols[i % 3]
    with col:
        # 두더지 위치에 따라 아이콘 변경
        if st.session_state.game_active and i in st.session_state.moles:
            label = "🐹"  # 두더지
        else:
            label = "🕳️"  # 빈 구멍

        st.button(
            label,
            key=f"hole_{i}",
            on_click=whack,
            args=(i,),
            disabled=not st.session_state.game_active,
            use_container_width=True,
        )
