#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 실제 AI 트레이딩 성과 대시보드
Real Trading Performance Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import pyupbit
import numpy as np
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv('key.env')

# 로컬 모듈
from database import TradingDatabase

# 페이지 설정
st.set_page_config(
    page_title="🚀 실제 AI 트레이딩 성과",
    page_icon="₿", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 고급 CSS 스타일링
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .sub-header {
        font-size: 1.8rem;
        color: #00D084;
        margin: 1rem 0;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        margin: 0.5rem 0;
    }
    .success-card {
        border-left-color: #00D084;
        background: linear-gradient(135deg, #0D2818 0%, #1E3A2E 100%);
    }
    .warning-card {
        border-left-color: #FFA500;
        background: linear-gradient(135deg, #2D1F0D 0%, #3D2F1D 100%);
    }
    .danger-card {
        border-left-color: #FF4757;
        background: linear-gradient(135deg, #2D0D0D 0%, #3D1D1D 100%);
    }
    .analysis-box {
        background: #1A1A1A;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #333;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        white-space: pre-wrap;
    }
    .trade-row-buy {
        background-color: rgba(0, 208, 132, 0.1);
        border-left: 4px solid #00D084;
    }
    .trade-row-sell {
        background-color: rgba(255, 71, 87, 0.1);
        border-left: 4px solid #FF4757;
    }
    .status-online {
        color: #00D084;
        font-weight: bold;
    }
    .status-offline {
        color: #FF4757;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_live_market_data():
    """실시간 시장 데이터"""
    try:
        current_price = pyupbit.get_current_price("KRW-BTC")
        df_daily = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=30)
        tickers = pyupbit.get_tickers(fiat="KRW")
        
        return {
            'current_price': current_price,
            'daily_data': df_daily,
            'status': 'online',
            'last_update': datetime.now(),
            'total_markets': len(tickers)
        }
    except Exception as e:
        st.error(f"⚠️ 시장 데이터 연결 실패: {str(e)}")
        return {'status': 'offline', 'error': str(e)}

@st.cache_data(ttl=30)
def get_real_account_balance():
    """실제 계좌 잔고 조회"""
    try:
        access_key = os.getenv('UPBIT_ACCESS_KEY')
        secret_key = os.getenv('UPBIT_SECRET_KEY')
        
        if not access_key or not secret_key:
            return {'status': 'no_api_key'}
        
        upbit = pyupbit.Upbit(access_key, secret_key)
        balances = upbit.get_balances()
        
        if isinstance(balances, str):
            return {'status': 'api_error', 'error': balances}
        
        account_data = {'KRW': 0, 'BTC': 0, 'total_assets': 0}
        
        for balance in balances:
            currency = balance.get('currency', '')
            balance_amount = float(balance.get('balance', 0))
            
            if currency == 'KRW':
                account_data['KRW'] = balance_amount
            elif currency == 'BTC':
                account_data['BTC'] = balance_amount
        
        # 현재 비트코인 가격으로 총 자산 계산
        current_price = pyupbit.get_current_price("KRW-BTC")
        btc_value = account_data['BTC'] * current_price
        account_data['total_assets'] = account_data['KRW'] + btc_value
        account_data['btc_value_krw'] = btc_value
        account_data['status'] = 'success'
        
        return account_data
        
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

@st.cache_data(ttl=300)
def load_trading_database():
    """거래 데이터베이스 로드"""
    try:
        db = TradingDatabase("trading_enhanced.db")
        
        # 모든 거래 내역을 가져오도록 수정 (날짜 필터 제거)
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        return {
            'recent_logs': db.get_recent_logs(100),
            'all_trades': db.get_trades_by_date(start_date, end_date),
            'portfolio_history': db.get_portfolio_history(90),
            'trading_stats': db.get_trading_stats(),
            'reflections': db.get_recent_reflections(20),
            'status': 'success'
        }
    except Exception as e:
        st.error(f"❌ 데이터베이스 로드 실패: {e}")
        return {'status': 'error', 'error': str(e)}

def render_real_time_status():
    """실시간 시스템 상태"""
    st.markdown('<h2 class="sub-header">🔴 LIVE 시스템 상태</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 시장 데이터 상태
    market_data = get_live_market_data()
    with col1:
        if market_data['status'] == 'online':
            st.markdown(f"""
            <div class="metric-card success-card">
                <h3>📈 시장 데이터</h3>
                <p class="status-online">● ONLINE</p>
                <p>₩{market_data['current_price']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card danger-card">
                <h3>📈 시장 데이터</h3>
                <p class="status-offline">● OFFLINE</p>
                <p>연결 실패</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 계좌 연결 상태
    account_data = get_real_account_balance()
    with col2:
        if account_data['status'] == 'success':
            st.markdown(f"""
            <div class="metric-card success-card">
                <h3>💰 실제 계좌</h3>
                <p class="status-online">● CONNECTED</p>
                <p>₩{account_data['total_assets']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            status_text = {
                'no_api_key': 'API 키 없음',
                'api_error': 'API 오류',
                'error': '연결 실패'
            }.get(account_data['status'], '알 수 없음')
            
            st.markdown(f"""
            <div class="metric-card danger-card">
                <h3>💰 실제 계좌</h3>
                <p class="status-offline">● DISCONNECTED</p>
                <p>{status_text}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 데이터베이스 상태
    db_data = load_trading_database()
    with col3:
        if db_data['status'] == 'success':
            st.markdown(f"""
            <div class="metric-card success-card">
                <h3>🗄️ 거래 DB</h3>
                <p class="status-online">● ACTIVE</p>
                <p>{len(db_data['recent_logs'])}개 로그</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card danger-card">
                <h3>🗄️ 거래 DB</h3>
                <p class="status-offline">● ERROR</p>
                <p>로드 실패</p>
            </div>
            """, unsafe_allow_html=True)
    
    # AI 트레이더 상태
    with col4:
        try:
            with open('latest_analysis.json', 'r', encoding='utf-8') as f:
                latest = json.load(f)
            
            analysis_time = datetime.fromisoformat(latest['timestamp'].replace('T', ' '))
            time_diff = datetime.now() - analysis_time
            
            if time_diff.total_seconds() < 3600:  # 1시간 이내
                status = "ACTIVE"
                status_class = "status-online"
                card_class = "success-card"
            else:
                status = "IDLE"
                status_class = "status-offline" 
                card_class = "warning-card"
                
            st.markdown(f"""
            <div class="metric-card {card_class}">
                <h3>🤖 AI 트레이더</h3>
                <p class="{status_class}">● {status}</p>
                <p>{latest['ai_decision']['decision']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        except:
            st.markdown(f"""
            <div class="metric-card danger-card">
                <h3>🤖 AI 트레이더</h3>
                <p class="status-offline">● OFFLINE</p>
                <p>분석 없음</p>
            </div>
            """, unsafe_allow_html=True)

def render_live_portfolio():
    """실시간 포트폴리오"""
    st.markdown('<h2 class="sub-header">💎 실시간 포트폴리오</h2>', unsafe_allow_html=True)
    
    account_data = get_real_account_balance()
    
    if account_data['status'] != 'success':
        st.error("❌ 실제 계좌 데이터를 불러올 수 없습니다.")
        st.info("💡 업비트 API 키가 설정되어 있는지 확인하세요.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💵 보유 현금 (KRW)",
            value=f"₩{account_data['KRW']:,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="🪙 보유 비트코인",
            value=f"{account_data['BTC']:.6f} BTC",
            delta=f"₩{account_data['btc_value_krw']:,.0f}"
        )
    
    with col3:
        total_assets = account_data['total_assets']
        st.metric(
            label="💎 총 자산",
            value=f"₩{total_assets:,.0f}",
            delta=None
        )
    
    with col4:
        btc_ratio = (account_data['btc_value_krw'] / total_assets * 100) if total_assets > 0 else 0
        st.metric(
            label="📊 BTC 비율",
            value=f"{btc_ratio:.1f}%",
            delta=f"현금 {100-btc_ratio:.1f}%"
        )
    
    # 포트폴리오 차트
    if total_assets > 0:
        fig = go.Figure(data=[go.Pie(
            labels=['KRW (현금)', 'BTC (비트코인)'],
            values=[account_data['KRW'], account_data['btc_value_krw']],
            hole=.3,
            marker_colors=['#FF6B35', '#00D084']
        )])
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            title="현재 자산 구성",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_detailed_analysis_logs():
    """상세 AI 분석 로그"""
    st.markdown('<h2 class="sub-header">🧠 AI 분석 로그 (상세)</h2>', unsafe_allow_html=True)
    
    db_data = load_trading_database()
    
    if db_data['status'] != 'success' or not db_data['recent_logs']:
        st.warning("분석 로그 데이터가 없습니다.")
        return
    
    # 필터 옵션
    col1, col2, col3 = st.columns(3)
    
    with col1:
        decision_filter = st.selectbox(
            "AI 결정 필터",
            ['전체', 'BUY', 'SELL', 'HOLD']
        )
    
    with col2:
        confidence_filter = st.selectbox(
            "신뢰도 필터", 
            ['전체', 'HIGH', 'MEDIUM', 'LOW']
        )
    
    with col3:
        limit = st.slider("표시 개수", 5, 50, 20)
    
    # 데이터 필터링
    logs = db_data['recent_logs'][:limit]
    
    if decision_filter != '전체':
        logs = [log for log in logs if log.get('ai_decision') == decision_filter]
    
    if confidence_filter != '전체':
        logs = [log for log in logs if log.get('ai_confidence') == confidence_filter]
    
    # 분석 로그 표시
    for i, log in enumerate(logs):
        with st.expander(f"📊 분석 #{i+1} - {log.get('ai_decision', 'N/A')} ({log.get('timestamp', 'N/A')})"):
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**📋 기본 정보**")
                st.write(f"🎯 **결정**: {log.get('ai_decision', 'N/A')}")
                st.write(f"🔒 **신뢰도**: {log.get('ai_confidence', 'N/A')}")
                st.write(f"💰 **BTC 가격**: ₩{log.get('current_price', 0):,.0f}")
                st.write(f"💵 **KRW 잔고**: ₩{log.get('krw_balance', 0):,.0f}")
                st.write(f"🪙 **BTC 잔고**: {log.get('btc_balance', 0):.6f}")
                
                # 시장 데이터 파싱 시도
                try:
                    market_data = json.loads(log.get('market_data_json', '{}'))
                    investment_status = market_data.get('investment_status', {})
                    
                    if investment_status:
                        st.markdown("**💎 포트폴리오**")
                        st.write(f"🏦 **총 자산**: ₩{investment_status.get('total_portfolio_value', 0):,.0f}")
                        st.write(f"📊 **BTC 비율**: {investment_status.get('btc_percentage', 0):.1f}%")
                except:
                    pass
            
            with col2:
                st.markdown("**🧠 AI 분석 상세 내용**")
                
                analysis_reason = log.get('ai_reason', '')
                if analysis_reason:
                    st.markdown(f"""
                    <div class="analysis-box">
{analysis_reason}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("상세 분석 내용이 없습니다.")
                
                # AI 분석 전체 데이터 표시
                try:
                    ai_full = json.loads(log.get('ai_analysis_full_json', '{}'))
                    if ai_full.get('trading_percentage'):
                        trading_pct = ai_full['trading_percentage']
                        st.markdown("**🎯 AI 거래 결정**")
                        if trading_pct.get('krw_to_invest', 0) > 0:
                            st.success(f"💰 매수 비율: {trading_pct['krw_to_invest']}%")
                        if trading_pct.get('btc_to_sell', 0) > 0:
                            st.error(f"🪙 매도 비율: {trading_pct['btc_to_sell']}%")
                except:
                    pass

def render_trading_performance():
    """실제 거래 성과"""
    st.markdown('<h2 class="sub-header">📈 실제 거래 성과</h2>', unsafe_allow_html=True)
    
    db_data = load_trading_database()
    
    if db_data['status'] != 'success':
        st.error("거래 데이터를 불러올 수 없습니다.")
        st.error(f"오류: {db_data.get('error', '알 수 없음')}")
        return
    
    trades = db_data['all_trades']
    
    if not trades:
        st.warning("❌ 거래 내역이 없습니다.")
        return
    
    # 거래 통계
    total_trades = len(trades)
    buy_trades = [t for t in trades if t.get('trade_type') == 'buy']
    sell_trades = [t for t in trades if t.get('trade_type') == 'sell']
    
    total_fees = sum(float(t.get('fee', 0)) for t in trades)
    total_buy_value = sum(float(t.get('total_value', 0)) for t in buy_trades)
    total_sell_value = sum(float(t.get('total_value', 0)) for t in sell_trades)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 거래 횟수", f"{total_trades}회")
    
    with col2:
        st.metric("매수 / 매도", f"{len(buy_trades)} / {len(sell_trades)}")
    
    with col3:
        st.metric("총 수수료", f"₩{total_fees:,.0f}")
    
    with col4:
        net_result = total_sell_value - total_buy_value
        st.metric("매매 차익", f"₩{net_result:,.0f}", 
                 delta=f"{(net_result/total_buy_value*100):.2f}%" if total_buy_value > 0 else None)
    
    # 거래 내역 테이블
    st.markdown("**📋 최근 거래 내역**")
    
    try:
        df_trades = pd.DataFrame(trades)
        if not df_trades.empty:
            # timestamp 컬럼을 사용 (실제 거래 시간)
            df_trades['timestamp'] = pd.to_datetime(df_trades['timestamp'])
            df_trades = df_trades.sort_values('timestamp', ascending=False)
            
            # 표시할 컬럼 선택 (실제 거래 시간 사용)
            display_data = []
            for trade in trades:
                display_data.append({
                    'timestamp': pd.to_datetime(trade.get('timestamp', '')),
                    'trade_type': trade.get('trade_type', ''),
                    'price': float(trade.get('price', 0)),
                    'amount': float(trade.get('amount', 0)),
                    'total_value': float(trade.get('total_value', 0)),
                    'fee': float(trade.get('fee', 0)),
                    'success': trade.get('success', False)
                })
            
            display_df = pd.DataFrame(display_data)
            display_df = display_df.sort_values('timestamp', ascending=False)
            
            # 포맷팅
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            display_df['price'] = display_df['price'].apply(lambda x: f"₩{x:,.0f}")
            display_df['amount'] = display_df['amount'].apply(lambda x: f"{x:.6f} BTC")
            display_df['total_value'] = display_df['total_value'].apply(lambda x: f"₩{x:,.0f}")
            display_df['fee'] = display_df['fee'].apply(lambda x: f"₩{x:,.0f}")
            
            display_df.columns = ['시간', '타입', '가격', '수량', '총액', '수수료', '성공']
            
            st.dataframe(display_df, use_container_width=True, height=400)
        else:
            st.warning("DataFrame이 비어있습니다.")
    except Exception as e:
        st.error(f"❌ 거래 내역 표시 중 오류: {e}")

def main():
    """메인 대시보드"""
    st.markdown('<h1 class="main-header">🚀 실제 AI 트레이딩 성과</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #888;">Real Performance Dashboard - Live Trading Results</p>', unsafe_allow_html=True)
    
    # 사이드바 메뉴
    st.sidebar.title("📊 대시보드 메뉴")
    page = st.sidebar.selectbox(
        "페이지 선택",
        ["🔴 실시간 상태", "💎 실시간 포트폴리오", "🧠 AI 분석 로그", "📈 거래 성과"]
    )
    
    # 새로고침 버튼
    if st.sidebar.button("🔄 데이터 새로고침"):
        st.cache_data.clear()
        st.rerun()
    
    # 시스템 정보
    st.sidebar.markdown("---")
    st.sidebar.markdown("**⚙️ 시스템 정보**")
    st.sidebar.info(f"🕒 마지막 업데이트: {datetime.now().strftime('%H:%M:%S')}")
    
    # 페이지 라우팅
    if page == "🔴 실시간 상태":
        render_real_time_status()
    
    elif page == "💎 실시간 포트폴리오":
        render_live_portfolio()
    
    elif page == "🧠 AI 분석 로그":
        render_detailed_analysis_logs()
    
    elif page == "📈 거래 성과":
        render_trading_performance()

if __name__ == "__main__":
    main() 
