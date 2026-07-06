import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="OptaPlanner Schedule Optimizer", page_icon="📅", layout="wide")

# 사이드바 상단에 언어 선택기 배치
lang_option = st.sidebar.radio("Language / 언어", ["English", "한국어"])
lang = "ko" if lang_option == "한국어" else "en"

# 번역 딕셔너리
T = {
    "title": {"ko": "📅 근무 스케줄링 최적화 비교 대시보드", "en": "📅 Schedule Optimization Dashboard"},
    "subtitle": {"ko": "OptaPlanner 엔진을 활용한 스케줄링 최적화 3단계 결과를 시각화합니다.", "en": "Visualizes the 3-stage scheduling optimization results using the OptaPlanner engine."},
    "settings": {"ko": "설정", "en": "Settings"},
    "select_model": {"ko": "비교할 모델을 선택하세요:", "en": "Select a model to compare:"},
    "m1_name": {"ko": "Model 1 (기본 튜닝)", "en": "Model 1 (Basic Tuning)"},
    "m2_name": {"ko": "Model 2 (공정성 제약)", "en": "Model 2 (Fairness)"},
    "m3_name": {"ko": "Model 3 (BAVET + 연속근무 방지)", "en": "Model 3 (BAVET + No Consecutive)"},
    "model_desc_title": {"ko": "💡 모델 설명", "en": "💡 Model Description"},
    "m1_desc": {"ko": "**Model 1**\n- Tabu Search + Late Acceptance\n- 공정성 제약 없음\n- 특정 직원에게 업무가 몰리는 현상 발생 가능", "en": "**Model 1**\n- Tabu Search + Late Acceptance\n- No fairness constraints\n- Workload may be concentrated on specific employees"},
    "m2_desc": {"ko": "**Model 2**\n- 근무 횟수의 제곱을 페널티로 부과\n- 업무량 분산 완료\n- 하지만 연속 5일 근무 등 피로도 문제 잔존", "en": "**Model 2**\n- Square of shifts penalized\n- Workload distributed evenly\n- However, fatigue issues like 5 consecutive working days remain"},
    "m3_desc": {"ko": "**Model 3**\n- 최신 BAVET 스트림 엔진 도입\n- Simulated Annealing 결합\n- 3일 연속 근무 시 기하급수적 페널티 부과 (징검다리 휴일 구현)", "en": "**Model 3**\n- BAVET stream engine\n- Simulated Annealing\n- Exponential penalty for 3+ consecutive days (creates rest days)"},
    "err_load": {"ko": "데이터를 불러오지 못했습니다:", "en": "Failed to load data:"},
    "err_no_data": {"ko": "스케줄 데이터가 없습니다.", "en": "No schedule data available."},
    "fairness_idx": {"ko": "공정성 지표 (최대-최소 차이)", "en": "Fairness Index (Max-Min diff)"},
    "fairness_unit": {"ko": "회", "en": "shifts"},
    "tab1": {"ko": "📅 스케줄 캘린더 (Table)", "en": "📅 Schedule Calendar"},
    "tab2": {"ko": "📊 연속 근무 차트 (Chart)", "en": "📊 Consecutive Work Chart"},
    "tab3": {"ko": "⚖️ 제약 조건 분석 (Penalty)", "en": "⚖️ Penalty Analysis"},
    "full_schedule": {"ko": "전체 근무 스케줄", "en": "Full Schedule"},
    "legend": {"ko": "A: 아침 (Morning) | P: 오후 (Afternoon) | L: 저녁 (Late) | V: 휴가 (Vacation) | H: 공휴일 (Holiday)", "en": "A: Morning | P: Afternoon | L: Late | V: Vacation | H: Holiday"},
    "max_consec_title": {"ko": "직원별 최대 연속 근무 일수 분석", "en": "Max Consecutive Working Days by Employee"},
    "guide_title": {"ko": "**분석 가이드:**", "en": "**Analysis Guide:**"},
    "guide_m12": {"ko": "- **Model 1 & 2**: 제약이 없어 누군가는 **5~6일 이상 휴일 없이 연속으로 과로**하는 현상이 나타납니다.", "en": "- **Model 1 & 2**: No constraints, causing some employees to be **overworked for 5~6 consecutive days** without a break."},
    "guide_m3": {"ko": "- **Model 3**: 연속 근무 방지 알고리즘 덕분에 **최대 3~4일 이내로 통제**되며 중간에 반드시 휴일(징검다리)이 배정됩니다.", "en": "- **Model 3**: Consecutive work prevention keeps it **under 3-4 days max**, ensuring proper rest days."},
    "penalty_title": {"ko": "제약 조건 위반 감점 내역", "en": "Constraint Violation Penalty Details"},
    "penalty_sub": {"ko": "현재 스케줄에서 어떤 규칙이 어겨져서 감점(Penalty)이 발생했는지 분석합니다.", "en": "Analyzes which rules were broken to cause penalties in the current schedule."},
    "penalty_perfect": {"ko": "감점 내역이 없습니다! 완벽한 스케줄입니다.", "en": "No penalties! Perfect schedule."}
}

def t(key):
    return T.get(key, {}).get(lang, key)

# 직원 매핑 정보
EMP_MAP = {
    "1": "Winter",
    "2": "Autumn",
    "3": "Summer",
    "4": "Spring",
    "5": "Karina"
}

# 솔루션 파일 경로
SOLUTION_DIR = "/Users/gyuminkang/Desktop/scheduling-optimization/opt_engine/apps/schedule-optimization-app/src/main/resources/solution-output/"

# 모델 키를 한국어/영어로 매핑
UI_MODELS = {
    t("m1_name"): "sol-20260705_005544-ac062041-6e9f-4066-832c-e3b93c5595c3.json",
    t("m2_name"): "sol-20260705_005945-50c9ac29-d69f-4b31-8133-1388965c9e5a.json",
    t("m3_name"): "sol-20260705_010523-5fc5e1ea-7190-4a49-b319-65a7230dbba5.json"
}

UI_INSPECTS = {
    t("m1_name"): "inspect-20260705_005546-ac062041-6e9f-4066-832c-e3b93c5595c3.json",
    t("m2_name"): "inspect-20260705_005945-50c9ac29-d69f-4b31-8133-1388965c9e5a.json",
    t("m3_name"): "inspect-20260705_010523-5fc5e1ea-7190-4a49-b319-65a7230dbba5.json"
}

def load_data(filename):
    filepath = os.path.join(SOLUTION_DIR, filename)
    with open(filepath, 'r') as f:
        return json.load(f)

# 커스텀 CSS 로드 (Professional & Premium Theme)
st.markdown("""
<style>
    /* 폰트 적용 (Inter) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* 전체 배경 미세조정 */
    .stApp {
        background-color: #0b0f19;
        background-image: radial-gradient(circle at top right, #1a233a, transparent 40%),
                          radial-gradient(circle at bottom left, #12182b, transparent 40%);
    }

    /* 메트릭 카드 글래스모피즘 & 애니메이션 */
    .metric-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.05), transparent);
        transform: skewX(-25deg);
        transition: all 0.7s;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.15);
    }
    
    .metric-card:hover::before {
        left: 200%;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #a8b1ff, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 8px;
    }
    
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* 탭 디자인 향상 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 8px 8px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        transition: background-color 0.3s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(51, 65, 85, 0.8);
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.1) !important;
        border-bottom: 2px solid #6366f1 !important;
    }

    /* 데이터프레임 (표) 모서리 둥글게 */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* 헤더 및 불필요한 요소 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 헤더
st.title(t("title"))
st.markdown(t("subtitle"))

# 사이드바
st.sidebar.title(t("settings"))
st.sidebar.markdown("---")
selected_model_name = st.sidebar.radio(t("select_model"), list(UI_MODELS.keys()))

st.sidebar.markdown("---")
st.sidebar.subheader(t("model_desc_title"))
if "Model 1" in selected_model_name:
    st.sidebar.success(t("m1_desc"))
elif "Model 2" in selected_model_name:
    st.sidebar.info(t("m2_desc"))
else:
    st.sidebar.warning(t("m3_desc"))

# 데이터 로드
try:
    data = load_data(UI_MODELS[selected_model_name])
    inspect_data = load_data(UI_INSPECTS[selected_model_name])
except Exception as e:
    st.error(f"{t('err_load')} {str(e)}")
    st.stop()

# 주요 메트릭 추출
score_str = data.get("score", "N/A")
duration_ms = data.get("solverDurationInMs", 0)

# 데이터프레임 변환
schedule_list = data.get("schedule", [])
if not schedule_list:
    st.warning(t("err_no_data"))
    st.stop()

df = pd.DataFrame(schedule_list)
# empNo를 이름으로 변경
df["Employee Name"] = df["empNo"].map(EMP_MAP)
df["Date"] = pd.to_datetime(df["date"], format="%Y%m%d").dt.strftime("%Y-%m-%d")

# 근무 타입 추출 (예: A614 -> A)
df["Shift Type"] = df["atndCode"].str[0]

# 피벗 테이블 생성 (직원 x 날짜)
pivot_df = df.pivot(index="Employee Name", columns="Date", values="Shift Type").fillna("-")

# 직원별 총 근무 횟수 계산
shift_counts = df.groupby("Employee Name").size().reset_index(name="Total Shifts")
max_shifts = shift_counts["Total Shifts"].max()
min_shifts = shift_counts["Total Shifts"].min()
shift_diff = max_shifts - min_shifts

# --- 메트릭 표시 ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Final Score</div><div class='metric-value'>{score_str}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Solver Duration</div><div class='metric-value'>{duration_ms} ms</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>{t('fairness_idx')}</div><div class='metric-value'>{shift_diff} {t('fairness_unit')}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 메인 뷰: 탭 형태 ---
tab1, tab2, tab3 = st.tabs([t("tab1"), t("tab2"), t("tab3")])

with tab1:
    st.subheader(f"{t('full_schedule')} ({selected_model_name})")
    
    # 스타일 함수
    def color_shifts(val):
        color = 'transparent'
        if val == 'A':
            color = 'rgba(76, 175, 80, 0.4)' # Green
        elif val == 'P':
            color = 'rgba(33, 150, 243, 0.4)' # Blue
        elif val == 'L':
            color = 'rgba(156, 39, 176, 0.4)' # Purple
        elif val == 'V':
            color = 'rgba(255, 152, 0, 0.4)' # Orange
        elif val == 'H':
            color = 'rgba(244, 67, 54, 0.4)' # Red
        return f'background-color: {color}'
    
    st.dataframe(pivot_df.style.map(color_shifts), use_container_width=True)
    st.caption(t("legend"))

# 연속 근무 일수 계산 함수
def get_max_consecutive(group):
    dates = pd.to_datetime(group["Date"]).sort_values()
    diffs = dates.diff().dt.days
    streaks = (diffs != 1).cumsum()
    return streaks.value_counts().max()

consecutive_df = df.groupby("Employee Name").apply(get_max_consecutive).reset_index(name="Max Consecutive Days")

with tab2:
    st.subheader(t("max_consec_title"))
    fig = px.bar(consecutive_df, x="Employee Name", y="Max Consecutive Days", color="Employee Name",
                 text="Max Consecutive Days", title="Max Consecutive Working Days per Employee",
                 template="plotly_dark", height=400)
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    {t('guide_title')}
    {t('guide_m12')}
    {t('guide_m3')}
    """)

with tab3:
    st.subheader(t("penalty_title"))
    st.markdown(t("penalty_sub"))
    
    constraints = inspect_data.get("constraintReport", [])
    if not constraints:
        st.info(t("penalty_perfect"))
    else:
        # 감점 내역을 DataFrame으로 변환
        penalty_list = []
        for c in constraints:
            caused_by = c.get("causedBy", "Unknown")
            # constraint 이름도 영어/한국어 처리 가능하지만 일단 그대로 둠 (JSON 데이터 기반)
            
            score = c.get("score", "")
            
            # extract soft score number for charting
            soft_score = 0
            if "soft" in score:
                try:
                    soft_score = int(score.split("/")[-1].replace("soft", ""))
                except:
                    pass
            
            penalty_list.append({"Constraint (Rule)": caused_by, "Score Penalty": score, "Soft Penalty": soft_score})
        
        penalty_df = pd.DataFrame(penalty_list)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.dataframe(penalty_df[["Constraint (Rule)", "Score Penalty"]], use_container_width=True)
        with col_b:
            if penalty_df["Soft Penalty"].min() <= 0:
                fig2 = px.bar(penalty_df, x="Constraint (Rule)", y="Soft Penalty", 
                              title="Soft Penalty by Constraint", template="plotly_dark", 
                              color="Soft Penalty", text="Soft Penalty")
                fig2.update_traces(textposition='outside')
                st.plotly_chart(fig2, use_container_width=True)
