# 🚀 AI Bitcoin Trading Dashboard - Real Performance

**실제 AI 트레이딩 시스템의 거래 성과를 보여주는 Streamlit 대시보드**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 프로젝트 개요

이 대시보드는 **실제로 운영 중인 AI 비트코인 트레이딩 시스템의 거래 성과**를 실시간으로 공개합니다. 
가상의 백테스팅이 아닌 **진짜 돈으로 진행된 실제 거래 결과**를 투명하게 보여줍니다.

🎯 **핵심 특징:**
- ✅ **실제 거래 데이터** - 업비트에서 실행된 진짜 거래 내역
- ✅ **AI 분석 로그** - 8섹션 기관급 상세 분석 리포트  
- ✅ **실시간 성과** - 현재 포트폴리오와 수익률 추적
- ✅ **투명한 공개** - 성공과 실패 모든 거래 기록 공개

## 🎬 대시보드 미리보기

### 🔴 실시간 시스템 상태
- 시장 데이터 연결 상태
- 실제 업비트 계좌 연결 상태  
- 거래 데이터베이스 상태
- AI 트레이더 활동 상태

### 💎 실시간 포트폴리오
- 실제 업비트 잔고 (KRW/BTC)
- 현재 자산 구성 및 비율
- 포트폴리오 가치 변화

### 🧠 AI 분석 로그
- 상세한 기술적 분석 (RSI, MACD, 볼린저밴드 등)
- 시장 심리 분석 (공포탐욕지수, 거래량 등)
- 뉴스 감정 분석 및 소셜 미디어 분석
- 리스크 관리 및 포지션 사이징 전략

### 📈 실제 거래 성과
- **전체 거래 통계** (총 거래 횟수, 매수/매도 비율, 수수료)
- **매매 손익** (총 수익, 수익률, 승률)
- **거래 내역 테이블** (시간, 가격, 수량, 성공여부)

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/ai-bitcoin-trading-dashboard.git
cd ai-bitcoin-trading-dashboard
```

### 2. 의존성 설치
```bash
pip install -r requirements_dashboard.txt
```

### 3. 대시보드 실행
```bash
streamlit run real_dashboard.py
```

### 4. 브라우저에서 확인
자동으로 열리거나 수동으로 접속: **http://localhost:8501**

## 📊 실제 거래 성과 데이터

이 대시보드에는 **실제 거래 데이터**가 포함되어 있습니다:

- 📅 **거래 기간**: 2025년 7월 2일 ~
- 🏦 **거래소**: 업비트 (Upbit)  
- 💰 **거래 화폐**: BTC/KRW
- 🤖 **AI 시스템**: GPT-4 기반 다중 지표 분석

### 현재 성과 (예시)
- 총 거래 횟수: **4회**
- 매수/매도: **4/0**  
- 평균 거래 금액: **~₩25,000**
- 수수료 총합: **₩46**

*실제 수치는 대시보드에서 실시간 확인 가능*

## 📁 파일 구조

```
📂 ai-bitcoin-trading-dashboard/
├── 📄 real_dashboard.py           # 🎯 메인 대시보드
├── 📄 database.py                 # 📊 데이터베이스 관리
├── 📄 requirements_dashboard.txt  # 📦 Python 패키지  
├── 📄 README.md                   # 📋 이 문서
├── 📄 trading_enhanced.db         # 🗄️ 실제 거래 데이터
└── 📄 .gitignore                  # 🔐 보안 설정
```

## 🔧 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Database**: SQLite  
- **Charts**: Plotly
- **API**: pyupbit (업비트 실시간 데이터)
- **AI Analysis**: GPT-4 기반 시장 분석

## 🎯 주요 기능 상세

### 🔍 기술적 분석
- **가격 지표**: SMA, EMA, 볼린저밴드
- **모멘텀**: RSI, MACD, 스토캐스틱  
- **변동성**: ATR, 변동성 지수
- **트렌드**: ADX, 지지/저항선

### 📰 시장 분석
- **감정 분석**: 뉴스, 소셜미디어
- **거래량 분석**: 기관/개인 비율
- **공포탐욕지수**: 시장 심리 측정

### ⚖️ 리스크 관리  
- **포지션 사이징**: 켈리 공식 기반
- **손절/익절**: 동적 목표가 설정
- **변동성 조정**: 시장 상황별 포지션 조절

## ⚠️ 중요 고지사항

- 📊 **성과 공개 목적**: 이 대시보드는 실제 AI 트레이딩 시스템의 성과를 투명하게 공개하기 위한 목적입니다
- 💡 **투자 조언 아님**: 표시된 내용은 투자 조언이 아니며, 모든 투자 결정은 본인 책임입니다
- 🔒 **민감 정보 제외**: API 키 등 민감한 정보는 제외되어 있습니다
- 📈 **실시간 데이터**: 일부 실시간 데이터는 인터넷 연결이 필요합니다

## 🤝 기여하기

1. Fork the Project
2. Create Feature Branch (`git checkout -b feature/NewFeature`)  
3. Commit Changes (`git commit -m 'Add NewFeature'`)
4. Push to Branch (`git push origin feature/NewFeature`)
5. Open Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

## 🙏 감사인사

- [Streamlit](https://streamlit.io/) - 웹 앱 프레임워크
- [pyupbit](https://github.com/sharebook-kr/pyupbit) - 업비트 API
- [Plotly](https://plotly.com/) - 인터랙티브 차트

---

⭐ **이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!** 

🔗 **실시간 대시보드 체험**: [GitHub Pages 배포 링크] (추후 추가)

💌 **문의 및 피드백**: Issues 탭에서 언제든 문의해주세요! 