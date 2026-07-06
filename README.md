<div align="center">

# 📅 직원 근무 스케줄링 최적화 엔진

<img src="images/streamlit_dashboard_premium.png" alt="Streamlit Dashboard" width="90%">

<br>

**OptaPlanner (BAVET Constraint Stream + 담금질 기법)** 기반으로 구축되고 프리미엄 **Streamlit 대시보드**로 시각화된 최고급 직원 근무 스케줄링 최적화 엔진입니다. 이 프로젝트는 직원의 공정성을 보장하고 번아웃을 방지하면서 비즈니스 요구사항을 완벽하게 충족하는 복잡한 인력 스케줄링(NP-Hard) 문제를 해결합니다.

</div>

---

## 🌟 Streamlit 최적화 대시보드

대화형 스트림릿(Streamlit) 대시보드를 통해 다양한 최적화 모델 간의 성능을 실시간으로 비교 분석할 수 있습니다. 각 제약 조건, 패널티 점수, 실행 시간 등을 평가하여 특정 스케줄이 왜 최적의 결과로 선택되었는지 직관적으로 이해할 수 있도록 돕습니다.

**주요 기능:**
- **다이내믹 스케줄 캘린더:** 아침, 오후, 저녁 등 근무 시간대별로 한눈에 들어오는 컬러 코딩 뷰 제공
- **공정성 지표(Fairness Index) 추적:** 직원들 간의 총 근무 횟수 격차를 수치화하여 모니터링
- **다국어 지원:** 영어와 한국어 UI 간의 손쉬운 토글 기능

---

## 🚀 Model 3 성능 및 결과 분석 (최종 완성본)

**Model 3**은 본 프로젝트의 가장 강력하고 고도화된 최종 최적화 엔진입니다. 최신 BAVET 스트림 처리 엔진과 메타휴리스틱(Simulated Annealing)을 결합하여 엄격한 공정성을 강제하고 연속 근무로 인한 피로를 사전에 방지합니다.

### 1. 최적의 스케줄 생성 (Optimal Schedule)
<p align="center">
  <img src="images/Model_3_schedule_table.png" alt="Model 3 Schedule" width="90%">
</p>
> *최종 스케줄은 직원들의 개인 휴무 요청, 공휴일, 그리고 필수 교대 근무 커버리지를 완벽하게 균형 맞추어 배정합니다.*

### 2. 번아웃 및 피로도 방지 (연속 근무 일수 제어)
<p align="center">
  <img src="images/Model_3_consecutive_chart.png" alt="Model 3 Consecutive Days" width="80%">
</p>
> *기존 모델들과 달리, Model 3은 직원 1인당 최대 연속 근무 일수를 3~4일 이내로 엄격하게 통제합니다. 연속 근무 사이에 반드시 징검다리 휴일을 배치하여 직원의 번아웃을 원천적으로 차단합니다.*

### 3. 제약 조건 위반 감점(Penalty) 분석
<p align="center">
  <img src="images/Model_3_penalty_chart.png" alt="Model 3 Penalties" width="80%">
</p>
> *최적화 엔진은 특정 규칙 위반(예: 휴무 요청 무시, 불공평한 업무 배분 등)에 대해 체계적으로 감점(Penalty)을 부과합니다. 이러한 Soft Penalty들은 알고리즘이 가장 인간 중심적인 스케줄을 짜도록 올바른 방향으로 유도합니다.*

---

## ⚙️ 모델 아키텍처 및 데이터 흐름도

### 1. 시스템 데이터 흐름 (System Data Flow)
<p align="center">
  <img src="images/architecture_diagram.png" alt="Architecture Diagram" width="80%">
</p>
> *초기 입력 데이터는 **BAVET Constraint Engine**으로 전달되어 초고속으로 제약 조건 점수를 계산합니다. **Simulated Annealing (담금질 기법)** 알고리즘은 이 점수를 바탕으로 수만 가지의 스케줄 조합을 탐색하며, 전역 최적해(Global Optimum)를 찾을 때까지 가장 좋은 해결책을 반복적으로 피드백합니다.*

### 2. 담금질 기법 최적화 시뮬레이션 (Simulated Annealing)
<p align="center">
  <img src="images/simulated_annealing_curve.png" alt="Simulated Annealing" width="80%">
</p>
> *탐색이 진행됨에 따라 알고리즘의 온도(자홍색 선)가 점차 하락합니다. 초반에는 지역 최적해(Local Optima)에 갇히는 것을 막기 위해 다소 좋지 않은 스케줄(연보라색 선)도 확률적으로 수용하지만, 온도가 식을수록 오직 가장 완벽한 스케줄(진보라색 선)만을 채택하여 최종 수렴합니다.*

---

## 📈 이전 모델들과의 비교 (Evolution & Baselines)

Model 3가 도출되기까지 거쳐온 과거의 베이스라인 모델들의 결과와 한계점입니다. 

### 🛑 Model 1 (기본 탐색 모델)
공정성 제약 없이 Tabu Search 알고리즘만 사용한 초창기 결과입니다.
<div align="center">
  <img src="images/Model_1_schedule_table.png" alt="Model 1 Schedule" width="80%"><br><br>
  <img src="images/Model_1_consecutive_chart.png" alt="Model 1 Consecutive" width="80%">
  <p><em>특정 직원에게 업무가 몰려 최대 6일까지 휴일 없이 연속으로 과로하는 현상이 뚜렷하게 발생했습니다.</em></p>
  <img src="images/Model_1_penalty_chart.png" alt="Model 1 Penalty" width="80%">
  <p><em>단순한 하드 제약조건만 피하고, 직원들의 피로도나 요청 휴무에 대한 Soft 패널티 제어가 미흡했습니다.</em></p>
</div>

### ⚠️ Model 2 (작업량 공정성 부여 모델)
전체 근무 횟수의 제곱을 페널티로 부과하여 총 업무량을 균등하게 분산시키려고 시도한 결과입니다.
<div align="center">
  <img src="images/Model_2_schedule_table.png" alt="Model 2 Schedule" width="80%"><br><br>
  <img src="images/Model_2_consecutive_chart.png" alt="Model 2 Consecutive" width="80%">
  <p><em>월간 총 업무량은 균등해졌으나, 특정 주에 일이 몰려 여전히 5일 이상 연속으로 근무하는 단기 피로도 문제는 전혀 해결되지 않았습니다.</em></p>
  <img src="images/Model_2_penalty_chart.png" alt="Model 2 Penalty" width="80%">
  <p><em>근무량 격차에 대한 페널티 점수는 최적화되었지만, 휴일 배치에 대한 질적인 최적화 로직이 부재했습니다.</em></p>
</div>

---

## 📂 프로젝트 폴더 구조

```text
.
├── infra/                  # 클라우드 리소스 배포를 위한 AWS CDK 코드
├── opt_engine/             # 핵심 최적화 엔진 로직
│   ├── apps/               # OptaPlanner 연동을 위한 Spring Boot / Quarkus REST API
│   ├── core/               # 도메인 모델 및 제약 조건(Constraints) 정의
│   └── streamlit_app/      # 파이썬 Streamlit 대시보드 및 시각화용 Jupyter Notebook
└── README.md
```

---

## 📚 데이터 출처 및 참고 문헌

- **핵심 최적화 엔진:** [OptaPlanner 공식 문서](https://www.optaplanner.org/learn/documentation.html) (Timefold로 전환 중)
- **대시보드 및 데이터 시각화:** [Streamlit](https://streamlit.io/) / [Plotly](https://plotly.com/)
- **클라우드 인프라 아키텍처:** [AWS Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/)
- **적용된 알고리즘 기법:** Simulated Annealing (담금질 기법), Tabu Search, Late Acceptance, BAVET Constraint Streams
