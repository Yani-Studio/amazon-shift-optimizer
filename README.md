<div align="center">

# 📅 직원 근무 스케줄링 최적화 엔진 (Amazon Shift Optimizer)

<img src="images/streamlit_dashboard_premium.png" alt="Streamlit Dashboard" width="90%">

<br>

**OptaPlanner (BAVET Constraint Stream + 담금질 기법)** 기반으로 구축되고 프리미엄 **Streamlit 대시보드**로 시각화된 최고급 직원 근무 스케줄링 최적화 엔진입니다. 이 프로젝트는 직원의 공정성을 보장하고 번아웃을 방지하면서 비즈니스 요구사항을 완벽하게 충족하는 복잡한 인력 스케줄링(NP-Hard) 문제를 해결합니다.

</div>

---

## 🌟 Streamlit 최적화 대시보드

기존의 최적화 엔진들은 내부 알고리즘이 어떻게 돌아가는지 알 수 없는 '블랙박스(Black-box)' 형태로 동작하는 경우가 많습니다. 본 프로젝트는 이를 해결하기 위해 파이썬 기반의 **대화형 스트림릿(Streamlit) 대시보드**를 구축하여 엔진의 의사결정 과정을 시각화했습니다.

이 대시보드를 통해 관리자는 다양한 최적화 모델(Model 1, 2, 3) 간의 성능을 실시간으로 비교 분석할 수 있습니다. 각 모델이 어떤 제약 조건을 어겼는지, 페널티 점수는 어떻게 부여되었는지, 실행 시간은 얼마나 걸렸는지를 직관적으로 파악하여 특정 스케줄이 최종 선택된 논리적 근거를 명확하게 이해할 수 있습니다.

**주요 기능:**
- **다이내믹 스케줄 캘린더:** 아침(M), 오후(A), 저녁(L) 등 근무 시간대별로 한눈에 들어오는 컬러 코딩 뷰 제공
- **공정성 지표(Fairness Index) 추적:** 직원들 간의 총 근무 횟수 격차를 수치화하여 모니터링
- **다국어 지원:** 영어(English)와 한국어 UI 간의 손쉬운 토글 기능

---

## 🚀 Model 3 성능 및 결과 분석 (최종 완성본)

**Model 3**은 본 프로젝트의 가장 강력하고 고도화된 최종 최적화 엔진입니다. 최신 BAVET 스트림 처리 엔진과 메타휴리스틱(Simulated Annealing)을 결합하여, 단순히 요구 인원수만 채우는 것을 넘어 **직원들의 삶의 질(Quality of Life)**을 보장하는 스케줄을 도출합니다.

### 1. 최적의 스케줄 생성 (Optimal Schedule)
<p align="center">
  <img src="images/Model_3_schedule_table.png" alt="Model 3 Schedule" width="90%">
</p>

> **결과 해석:** 최종 도출된 스케줄표입니다. 빈칸은 휴무일을 의미하며, 직원들의 개인 휴무 요청, 공휴일 스케줄, 그리고 병원/매장의 필수 교대 근무 커버리지(M/A/L)를 완벽하게 균형 맞추어 배정했습니다. 단순히 빈자리를 채우는 것이 아니라, 각 직원의 숙련도(Skill)를 고려하여 교대조를 편성합니다.

### 2. 번아웃 및 피로도 방지 (연속 근무 일수 제어)
<p align="center">
  <img src="images/Model_3_consecutive_chart.png" alt="Model 3 Consecutive Days" width="80%">
</p>

> **결과 해석:** 이 차트는 각 직원이 최대 며칠을 연속으로 근무했는지를 보여줍니다. 기존의 최적화 모델들은 인력 부족 시 특정 직원에게 5~6일 연속 근무를 배정하는 치명적인 단점이 있었습니다. 반면, **Model 3은 직원 1인당 최대 연속 근무 일수를 3~4일 이내로 엄격하게 통제**합니다. 연속 근무 사이에 반드시 '징검다리 휴일'을 강제로 배치하여 직원의 번아웃과 과로를 원천적으로 차단합니다.

### 3. 제약 조건 위반 감점(Penalty) 분석
<p align="center">
  <img src="images/Model_3_penalty_chart.png" alt="Model 3 Penalties" width="80%">
</p>

> **결과 해석:** 완벽한 스케줄이란 사실상 존재하지 않습니다(NP-Hard). 휴무 요청을 다 들어주면 인력이 부족하고, 인력을 채우면 연속 근무가 발생합니다. 최적화 엔진은 특정 규칙 위반(예: 휴무 요청 무시, 불공평한 업무 배분 등)에 대해 체계적으로 감점(Penalty)을 부과합니다. 위 차트는 최종 스케줄에서 어쩔 수 없이 감점된 내역을 보여줍니다. 이러한 Soft Penalty 가중치 조정은 알고리즘이 가장 '인간 중심적인' 스케줄을 짜도록 올바른 방향으로 유도하는 핵심 역할을 합니다.

---

## ⚙️ 모델 아키텍처 및 데이터 흐름도

수천만 개의 스케줄 조합 중 최고의 스케줄을 1분 안에 찾아내는 내부 엔진의 수학적, 구조적 원리입니다.

### 1. 시스템 데이터 흐름 (System Data Flow)
<p align="center">
  <img src="images/architecture_diagram.png" alt="Architecture Diagram" width="80%">
</p>

> **기술 설명:** 
> 초기 입력 데이터(직원 정보, 스킬, 교대근무 셋)는 **BAVET Constraint Engine**으로 전달됩니다. BAVET 엔진의 가장 큰 특징은 **'점진적 점수 계산(Incremental Calculation)'**입니다. 스케줄이 하나 바뀔 때마다 전체 점수를 재계산하는 것이 아니라, 변경된 부분의 점수만 초고속으로 업데이트합니다.
> 이 초고속 점수 평가를 바탕으로 **Simulated Annealing (담금질 기법)** 알고리즘이 수만 가지의 스케줄 조합을 끊임없이 탐색하며, 전역 최적해(Global Optimum)를 찾을 때까지 피드백 루프를 반복합니다.

### 2. 담금질 기법 최적화 시뮬레이션 (Simulated Annealing)
<p align="center">
  <img src="images/simulated_annealing_curve.png" alt="Simulated Annealing" width="80%">
</p>

> **기술 설명:** 
> 금속을 달구었다가 천천히 식히며 단단하게 만드는 '담금질'에서 착안한 알고리즘입니다. 탐색이 진행됨에 따라 알고리즘의 **온도(Temperature, 자홍색 선)**가 점차 하락합니다. 
> - **초반 (온도가 높을 때):** 단순히 현재보다 좋은 스케줄만 고집하면 지역 최적해(Local Optima)에 갇히게 됩니다. 따라서 초반에는 다소 점수가 떨어지는 나쁜 스케줄(연보라색 선)도 확률적으로 수용하여 넓은 범위를 탐색합니다.
> - **후반 (온도가 낮을 때):** 온도가 식을수록 알고리즘은 깐깐해집니다. 오직 과거보다 더 완벽한 스케줄(진보라색 선)만을 엄격하게 채택하여 최종적으로 가장 이상적인 스케줄에 안착합니다.

---

## 📈 이전 모델들과의 비교 (Evolution & Baselines)

초기 모델부터 현재의 Model 3까지, 엔진이 어떻게 진화하고 문제를 해결해 왔는지 보여주는 히스토리입니다.

### 🛑 Model 1 (기본 탐색 모델)
아무런 공정성 제약 없이 가장 기본적인 알고리즘(Tabu Search)만 적용했던 초기 모델입니다. 필수 근무 인원을 채우는 데에만 급급했습니다.
<div align="center">
  <img src="images/Model_1_schedule_table.png" alt="Model 1 Schedule" width="80%"><br><br>
  <img src="images/Model_1_consecutive_chart.png" alt="Model 1 Consecutive" width="80%">
  <p><em>⚠️ <b>문제점:</b> 특정 소수의 직원에게 업무가 극단적으로 몰려, <b>최대 6일까지 휴일 없이 연속으로 과로</b>하는 현상이 뚜렷하게 발생했습니다. 이는 실제 업무 환경에 절대 도입할 수 없는 스케줄이었습니다.</em></p>
  <img src="images/Model_1_penalty_chart.png" alt="Model 1 Penalty" width="80%">
  <p><em>단순한 인원수 맞추기 위주의 하드 제약조건만 피하고, 직원들의 피로도나 요청 휴무에 대한 유연한 패널티 제어가 전혀 이루어지지 않았습니다.</em></p>
</div>

### ⚠️ Model 2 (작업량 공정성 부여 모델)
Model 1의 문제를 해결하기 위해, 전체 근무 횟수의 제곱을 페널티로 부과(Squared Penalty)하여 총 업무량을 균등하게 분산시키려고 시도한 개선 모델입니다.
<div align="center">
  <img src="images/Model_2_schedule_table.png" alt="Model 2 Schedule" width="80%"><br><br>
  <img src="images/Model_2_consecutive_chart.png" alt="Model 2 Consecutive" width="80%">
  <p><em>⚠️ <b>문제점:</b> 한 달 전체를 기준으로 한 '총 업무량'은 직원들 사이에 공평하게 나뉘었습니다. 하지만 특정 주차에 일이 몰리는 배치를 막지 못해, 여전히 <b>5일 이상 연속으로 근무하는 단기 번아웃 문제</b>는 전혀 해결되지 않았습니다.</em></p>
  <img src="images/Model_2_penalty_chart.png" alt="Model 2 Penalty" width="80%">
  <p><em>근무량 격차 페널티 점수는 최적화되었지만, 휴일을 언제, 어떻게 배치할 것인지에 대한 질적인 최적화 로직이 부재했습니다. 이 한계를 극복하기 위해 Model 3가 탄생했습니다.</em></p>
</div>

---

## 📂 프로젝트 폴더 구조

```text
.
├── infra/                  # 클라우드 리소스 배포를 위한 AWS CDK 코드 (IaC)
├── opt_engine/             # 핵심 최적화 엔진 로직
│   ├── apps/               # OptaPlanner 연동을 위한 Spring Boot / Quarkus REST API
│   ├── core/               # 도메인 모델, Entity, 제약 조건(Constraints) 로직 정의
│   └── streamlit_app/      # 파이썬 Streamlit 대시보드 프론트엔드 및 데이터 분석용 Jupyter Notebook
└── README.md
```

---

## 📚 데이터 출처 및 참고 문헌

- **핵심 최적화 엔진:** [OptaPlanner 공식 문서](https://www.optaplanner.org/learn/documentation.html) (현재 차세대 엔진 Timefold로 전환 중)
- **대시보드 및 데이터 시각화:** 파이썬 오픈소스 프레임워크 [Streamlit](https://streamlit.io/) 및 인터랙티브 차트 라이브러리 [Plotly](https://plotly.com/)
- **클라우드 인프라 아키텍처:** 아마존 웹 서비스의 코드로 관리하는 인프라 [AWS Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/)
- **적용된 알고리즘 기법:** 메타휴리스틱 (Simulated Annealing 담금질 기법, Tabu Search), BAVET Constraint Streams 알고리즘
