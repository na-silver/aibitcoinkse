# 🚀 비트코인 매매 대시보드

Streamlit 기반 비트코인 매매 기록 분석 및 시각화 대시보드입니다.

## 📋 개요

이 대시보드는 **실제 AI 트레이딩 시스템의 성과**를 실시간으로 보여줍니다. 별도의 AI 트레이딩 봇이 비트코인 매매를 수행하고, 해당 시스템에서 생성된 **실제 거래 데이터**를 시각화합니다.

🎯 **실제 트레이딩 성과 공개** - 이론이 아닌 실전 데이터로 AI 트레이딩 시스템의 성능을 증명합니다.

## ✨ 주요 기능

### 🏠 메인 대시보드
- 현재 비트코인 가격 (실시간)
- 총 분석/거래 횟수, 승률 등 주요 지표
- 비트코인 가격 차트 (캔들스틱)
- 최신 AI 분석 결과
- 매매 전략 분석 (과열장/저점 신호)

### ⚡ 실시간 분석
- 실시간 가격 및 24시간 통계
- 기술적 지표 (RSI, 이동평균)
- 과매수/과매도 상태 분석

### 💰 매매 기록
- 전체 거래 통계
- 최근 거래 내역 테이블
- 거래 포인트 시각화 차트

### 📊 포트폴리오
- 포트폴리오 가치 변화 추이
- 일별 수익률 차트
- 현재 자산 구성 (KRW/BTC 비율)

### 🧠 AI 반성 일지
- AI 자가 분석 및 반성 내용
- 전략 성과 분석
- AI 결정 분포 차트

### 📋 분석 로그
- 상세한 AI 분석 기록
- 필터링 옵션 (매수/매도/관망)
- 고급 전략 분석 결과

## 🚀 시작하기

### 필수 요구사항
- Python 3.8+
- SQLite 데이터베이스 (trading_enhanced.db)

### 설치 방법

1. **저장소 클론**
```bash
git clone https://github.com/your-username/bitcoin-trading-dashboard.git
cd bitcoin-trading-dashboard
```

2. **의존성 설치**
```bash
pip install -r requirements_dashboard.txt
```

3. **대시보드 실행**
```bash
streamlit run streamlit_dashboard.py
```

4. **브라우저에서 접속**
- 자동으로 브라우저가 열리거나
- 수동으로 `http://localhost:8501` 접속

### 데이터베이스 구조

대시보드는 다음 테이블을 사용합니다:

- `trading_logs`: AI 분석 로그
- `actual_trades`: 실제 거래 기록  
- `portfolio_snapshots`: 포트폴리오 스냅샷
- `self_reflections`: AI 자기반성 기록

## 📁 파일 구조

```
bitcoin-trading-dashboard/
├── streamlit_dashboard.py    # 메인 대시보드 앱
├── database.py              # 데이터베이스 관리 클래스
├── requirements_dashboard.txt # 필요한 Python 패키지
├── README.md               # 이 파일
└── trading_enhanced.db     # SQLite 데이터베이스 (별도 생성)
```

## 🔧 설정 및 사용법

### 오프라인 모드
시장 데이터 API 연결이 안 되는 경우, 자동으로 오프라인 모드로 전환됩니다.
- 데이터베이스의 기록된 데이터만 표시
- 실시간 차트는 비활성화
- 모든 분석 기능은 정상 작동

### 데이터베이스 연결
- 기본 데이터베이스 파일: `trading_enhanced.db`
- 파일이 없으면 빈 테이블로 자동 생성
- 실제 매매 데이터는 별도 트레이딩 시스템에서 생성

### 캐시 설정
- 시장 데이터: 1분마다 새로고침
- 데이터베이스 데이터: 5분마다 새로고침

## 🎯 사용 사례

1. **매매 성과 분석**: 과거 거래 내역과 수익률 확인
2. **AI 전략 검증**: AI 분석의 정확도와 패턴 파악  
3. **포트폴리오 모니터링**: 자산 구성과 변화 추적
4. **시장 분석**: 기술적 지표와 시장 상황 파악

## ⚠️ 주의사항

- **이 대시보드는 성과 분석 전용입니다** - 실제 매매 기능은 없습니다 (별도 시스템에서 진행)
- **실제 트레이딩 데이터**가 포함되어 있어 투자 성과를 확인할 수 있습니다
- 실시간 데이터는 pyupbit API를 사용하므로 인터넷 연결이 필요합니다
- 데이터베이스는 읽기 전용으로만 사용됩니다 (실제 거래는 별도 시스템)

## 🔗 관련 링크

- [Streamlit 문서](https://docs.streamlit.io/)
- [Plotly 문서](https://plotly.com/python/)
- [pyupbit 문서](https://github.com/sharebook-kr/pyupbit)

## 📄 라이선스

MIT License

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 문의

프로젝트에 대한 질문이나 제안이 있으시면 이슈를 생성해주세요.

---

⭐ **이 프로젝트가 도움이 되셨다면 별표를 눌러주세요!** 