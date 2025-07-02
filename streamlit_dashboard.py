#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 비트코인 매매 대시보드 - Streamlit 웹 대시보드
데이터베이스를 활용한 매매 기록 분석 및 시각화 플랫폼
GitHub 업로드용 버전 (트레이딩 로직 의존성 제거)
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

# 로컬 모듈 import
from database import TradingDatabase

# 페이지 설정
st.set_page_config(
    page_title="🚀 비트코인 매매 대시보드",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B35;
    }
    .success-metric {
        border-left-color: #00D084;
    }
    .warning-metric {
        border-left-color: #FFA500;
    }
    .danger-metric {
        border-left-color: #FF4757;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)  # 1분 캐시
def load_current_market_data():
    """현재 시장 데이터 로드"""
    try:
        current_price = pyupbit.get_current_price("KRW-BTC")
        df_daily = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=30)
        df_minute = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=24)
        
        return {
            'current_price': current_price,
            'daily_data': df_daily,
            'hourly_data': df_minute,
            'last_update': datetime.now()
        }
    except Exception as e:
        st.error(f"시장 데이터 로드 실패: {e}")
        return None

@st.cache_data(ttl=300)  # 5분 캐시
def load_database_data():
    """데이터베이스 데이터 로드"""
    try:
        db = TradingDatabase("trading_enhanced.db")
        
        return {
            'recent_logs': db.get_recent_logs(50),
            'recent_trades': db.get_trades_by_date((datetime.now() - timedelta(days=30)).isoformat()),
            'portfolio_history': db.get_portfolio_history(30),
            'trading_stats': db.get_trading_stats(),
            'recent_reflections': db.get_recent_reflections(10)
        }
    except Exception as e:
        st.error(f"데이터베이스 로드 실패: {e}")
        return {
            'recent_logs': [],
            'recent_trades': [],
            'portfolio_history': [],
            'trading_stats': {},
            'recent_reflections': []
        }

def render_main_dashboard():
    """메인 대시보드 페이지"""
    st.markdown('<h1 class="main-header">₿ 비트코인 매매 대시보드</h1>', unsafe_allow_html=True)
    
    # 실시간 데이터 로드
    market_data = load_current_market_data()
    db_data = load_database_data()
    
    if not market_data:
        st.warning("시장 데이터를 불러올 수 없습니다. 오프라인 모드로 실행됩니다.")
        # 오프라인 모드에서는 DB 데이터만 표시
        if db_data['recent_logs']:
            latest_log = db_data['recent_logs'][0]
            current_price = latest_log.get('current_price', 0)
        else:
            current_price = 0
    else:
        current_price = market_data['current_price']
    
    # 상단 메트릭 카드
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if market_data and len(market_data['daily_data']) > 1:
            delta = f"{((current_price / market_data['daily_data']['close'][-2]) - 1) * 100:.2f}%"
        else:
            delta = None
        
        st.metric(
            label="🔥 현재 비트코인 가격",
            value=f"₩{current_price:,.0f}" if current_price else "데이터 없음",
            delta=delta
        )
    
    with col2:
        total_logs = len(db_data['recent_logs'])
        st.metric(
            label="📊 총 분석 횟수",
            value=f"{total_logs}회",
            delta="전체 기간"
        )
    
    with col3:
        total_trades = len(db_data['recent_trades'])
        st.metric(
            label="💰 총 거래 횟수", 
            value=f"{total_trades}회",
            delta="최근 30일"
        )
    
    with col4:
        win_rate = db_data['trading_stats'].get('overall_win_rate', 0)
        st.metric(
            label="🎯 전체 승률",
            value=f"{win_rate:.1f}%",
            delta="전체 기간"
        )
    
    st.divider()
    
    # 차트 섹션
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 비트코인 가격 차트")
        
        if market_data:
            # 캔들스틱 차트
            fig = go.Figure(data=go.Candlestick(
                x=market_data['daily_data'].index,
                open=market_data['daily_data']['open'],
                high=market_data['daily_data']['high'],
                low=market_data['daily_data']['low'],
                close=market_data['daily_data']['close'],
                name="BTC-KRW"
            ))
            
            fig.update_layout(
                title="비트코인 일봉 차트 (30일)",
                yaxis_title="가격 (KRW)",
                xaxis_title="날짜",
                template="plotly_dark",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("시장 데이터를 사용할 수 없습니다.")
    
    with col2:
        st.subheader("🤖 최신 AI 분석")
        
        if db_data['recent_logs']:
            latest_log = db_data['recent_logs'][0]
            
            # AI 결정 표시
            decision = latest_log.get('ai_decision', 'UNKNOWN')
            confidence = latest_log.get('ai_confidence', 'UNKNOWN')
            
            if decision == 'BUY':
                st.success(f"🔥 **{decision}** (신뢰도: {confidence})")
            elif decision == 'SELL':
                st.error(f"🚨 **{decision}** (신뢰도: {confidence})")
            else:
                st.info(f"⏳ **{decision}** (신뢰도: {confidence})")
            
            # AI 분석 이유
            reason = latest_log.get('ai_reason', '분석 이유 없음')
            st.write("**분석 근거:**")
            st.write(reason[:200] + "..." if len(reason) > 200 else reason)
            
            # 상세 AI 분석 정보 표시
            try:
                ai_analysis_json = latest_log.get('ai_analysis_full_json', '{}')
                if ai_analysis_json and ai_analysis_json != '{}':
                    ai_analysis = json.loads(ai_analysis_json)
                    
                    # 기술적 지표 표시
                    if 'technical_indicators' in ai_analysis:
                        indicators = ai_analysis['technical_indicators']
                        st.write("**📊 기술적 지표:**")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if 'rsi' in indicators:
                                rsi_val = indicators['rsi']
                                rsi_color = "🔴" if rsi_val > 70 else "🟢" if rsi_val < 30 else "🟡"
                                st.write(f"{rsi_color} RSI: **{rsi_val:.1f}**")
                            
                            if 'trend' in indicators:
                                trend = indicators['trend']
                                trend_emoji = "📈" if trend == "상승" else "📉" if trend == "하락" else "➡️"
                                st.write(f"{trend_emoji} 트렌드: **{trend}**")
                        
                        with col_b:
                            if 'sma_5' in indicators:
                                st.write(f"📊 SMA5: **{indicators['sma_5']:,.0f}**")
                            if 'sma_20' in indicators:
                                st.write(f"📊 SMA20: **{indicators['sma_20']:,.0f}**")
                    
                    # 시장 감정 및 위험도
                    sentiment = ai_analysis.get('market_sentiment', '')
                    risk_level = ai_analysis.get('risk_level', '')
                    
                    if sentiment or risk_level:
                        st.write("**🎯 시장 분석:**")
                        if sentiment:
                            sentiment_emoji = "😄" if sentiment == "낙관적" else "😰" if sentiment == "비관적" else "😐"
                            st.write(f"{sentiment_emoji} 시장 감정: **{sentiment}**")
                        if risk_level:
                            risk_emoji = "🔥" if risk_level == "HIGH" else "⚡" if risk_level == "MEDIUM" else "✅"
                            st.write(f"{risk_emoji} 위험도: **{risk_level}**")
                            
            except Exception as e:
                st.caption("상세 분석 정보 파싱 실패")
            
            # 분석 시간
            timestamp = latest_log.get('timestamp', '')
            if timestamp:
                try:
                    # ISO 형식 시간을 읽기 쉽게 변환
                    from datetime import datetime
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%m-%d %H:%M')
                    st.caption(f"🕐 분석 시간: {formatted_time}")
                except:
                    st.caption(f"🕐 분석 시간: {timestamp[:16]}")
        
        else:
            st.warning("분석 데이터가 없습니다.")
    
    st.divider()
    
    # 고급 전략 분석 섹션 (DB에서 가져온 데이터 기준)
    st.subheader("🎯 매매 전략 분석 (DB 기록 기준)")
    
    if db_data['recent_logs']:
        latest_log = db_data['recent_logs'][0]
        try:
            market_data_json = json.loads(latest_log.get('market_data_json', '{}'))
            advanced_analysis = market_data_json.get('advanced_strategy_analysis', {})
            
            if advanced_analysis:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    overheated = advanced_analysis.get('overheated_analysis', {})
                    level = overheated.get('overheated_level', 'NONE')
                    signals = overheated.get('total_signals', 0)
                    
                    if level == 'EXTREME':
                        st.error(f"🔥 과열장 신호: **{level}** ({signals}개)")
                    elif level == 'MODERATE':
                        st.warning(f"🔥 과열장 신호: **{level}** ({signals}개)")
                    elif level == 'MILD':
                        st.info(f"🔥 과열장 신호: **{level}** ({signals}개)")
                    else:
                        st.success(f"🔥 과열장 신호: **없음**")
                
                with col2:
                    bottom = advanced_analysis.get('bottom_buying_analysis', {})
                    level = bottom.get('bottom_level', 'NONE')
                    signals = bottom.get('total_signals', 0)
                    
                    if level == 'STRONG':
                        st.success(f"📉 저점 신호: **{level}** ({signals}개)")
                    elif level == 'MODERATE':
                        st.info(f"📉 저점 신호: **{level}** ({signals}개)")
                    elif level == 'MILD':
                        st.warning(f"📉 저점 신호: **{level}** ({signals}개)")
                    else:
                        st.info(f"📉 저점 신호: **없음**")
                
                with col3:
                    final_rec = advanced_analysis.get('final_recommendation', {})
                    action = final_rec.get('action', 'HOLD')
                    percentage = final_rec.get('percentage', 0)
                    
                    if action == 'BUY':
                        st.success(f"💰 권고: **{action}** ({percentage}%)")
                    elif action == 'SELL':
                        st.error(f"💰 권고: **{action}** ({percentage}%)")
                    else:
                        st.info(f"💰 권고: **{action}**")
            else:
                st.info("고급 전략 분석 데이터가 없습니다.")
            
        except Exception as e:
            st.warning("고급 전략 분석 데이터 파싱 실패")
    else:
        st.info("분석 데이터가 없습니다.")

def render_realtime_analysis():
    """실시간 분석 페이지"""
    st.markdown('<h1 class="main-header">⚡ 실시간 시장 분석</h1>', unsafe_allow_html=True)
    
    market_data = load_current_market_data()
    if not market_data:
        st.error("시장 데이터를 불러올 수 없습니다.")
        return
    
    # 실시간 가격 표시
    col1, col2, col3 = st.columns(3)
    
    current_price = market_data['current_price']
    daily_data = market_data['daily_data']
    
    with col1:
        prev_price = daily_data['close'][-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        st.metric(
            label="현재 가격",
            value=f"₩{current_price:,.0f}",
            delta=f"{change:+,.0f} ({change_pct:+.2f}%)"
        )
    
    with col2:
        high_24h = daily_data['high'][-1]
        low_24h = daily_data['low'][-1]
        
        st.metric(
            label="24시간 고가",
            value=f"₩{high_24h:,.0f}"
        )
        st.metric(
            label="24시간 저가", 
            value=f"₩{low_24h:,.0f}"
        )
    
    with col3:
        volume = daily_data['volume'][-1]
        st.metric(
            label="24시간 거래량",
            value=f"{volume:,.2f} BTC"
        )
    
    st.divider()
    
    # 기술적 지표 계산 및 표시
    st.subheader("📊 기술적 지표")
    
    # RSI 계산
    def calculate_rsi(prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    # 이동평균 계산
    sma_20 = daily_data['close'].rolling(20).mean()
    sma_50 = daily_data['close'].rolling(50).mean() if len(daily_data) >= 50 else None
    rsi = calculate_rsi(daily_data['close'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 가격 + 이동평균 차트
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_data.index,
            y=daily_data['close'],
            mode='lines',
            name='비트코인 가격',
            line=dict(color='orange', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_data.index,
            y=sma_20,
            mode='lines',
            name='SMA 20',
            line=dict(color='blue', width=1)
        ))
        
        if sma_50 is not None:
            fig.add_trace(go.Scatter(
                x=daily_data.index,
                y=sma_50,
                mode='lines',
                name='SMA 50',
                line=dict(color='red', width=1)
            ))
        
        fig.update_layout(
            title="가격 및 이동평균",
            yaxis_title="가격 (KRW)",
            template="plotly_dark",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # RSI 차트
        fig_rsi = go.Figure()
        
        fig_rsi.add_trace(go.Scatter(
            x=daily_data.index,
            y=rsi,
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=2)
        ))
        
        # 과매수/과매도 라인
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="과매수")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="과매도")
        fig_rsi.add_hline(y=50, line_dash="dot", line_color="gray", annotation_text="중립")
        
        fig_rsi.update_layout(
            title="RSI (14일)",
            yaxis_title="RSI",
            yaxis=dict(range=[0, 100]),
            template="plotly_dark",
            height=300
        )
        
        st.plotly_chart(fig_rsi, use_container_width=True)
    
    # 현재 기술적 지표 값
    st.subheader("🎯 현재 기술적 지표 값")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 0
        if current_rsi > 70:
            st.error(f"RSI: {current_rsi:.1f} (과매수)")
        elif current_rsi < 30:
            st.success(f"RSI: {current_rsi:.1f} (과매도)")
        else:
            st.info(f"RSI: {current_rsi:.1f} (중립)")
    
    with col2:
        current_sma20 = sma_20.iloc[-1]
        if current_price > current_sma20:
            st.success(f"SMA20 상회")
        else:
            st.error(f"SMA20 하회")
        st.caption(f"SMA20: ₩{current_sma20:,.0f}")
    
    with col3:
        if sma_50 is not None:
            current_sma50 = sma_50.iloc[-1]
            if current_price > current_sma50:
                st.success(f"SMA50 상회")
            else:
                st.error(f"SMA50 하회")
            st.caption(f"SMA50: ₩{current_sma50:,.0f}")
    
    with col4:
        # 거래량 분석
        avg_volume = daily_data['volume'].rolling(10).mean().iloc[-1]
        current_volume = daily_data['volume'].iloc[-1]
        
        if current_volume > avg_volume * 1.5:
            st.warning("거래량 급증")
        elif current_volume < avg_volume * 0.5:
            st.info("거래량 저조")
        else:
            st.success("거래량 정상")
        
        st.caption(f"현재: {current_volume:.2f} BTC")

def render_trading_history():
    """매매 기록 페이지"""
    st.markdown('<h1 class="main-header">💰 매매 기록 & 성과 분석</h1>', unsafe_allow_html=True)
    
    db_data = load_database_data()
    
    # 거래 통계
    st.subheader("📊 거래 통계")
    
    stats = db_data['trading_stats']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 거래 횟수", f"{stats.get('total_trades', 0)}회")
    
    with col2:
        st.metric("성공 거래", f"{stats.get('successful_trades', 0)}회")
    
    with col3:
        st.metric("실패 거래", f"{stats.get('failed_trades', 0)}회")
    
    with col4:
        win_rate = stats.get('overall_win_rate', 0)
        st.metric("전체 승률", f"{win_rate:.1f}%")
    
    st.divider()
    
    # 최근 거래 내역
    st.subheader("📝 최근 거래 내역")
    
    if db_data['recent_trades']:
        trades_df = pd.DataFrame(db_data['recent_trades'])
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        trades_df = trades_df.sort_values('timestamp', ascending=False)
        
        # 거래 타입별 색상 지정
        def color_trade_type(val):
            if val == 'buy':
                return 'background-color: rgba(0, 208, 132, 0.3)'
            elif val == 'sell':
                return 'background-color: rgba(255, 71, 87, 0.3)'
            return ''
        
        styled_df = trades_df[['timestamp', 'trade_type', 'price', 'amount', 'total_value', 'success']].style.applymap(
            color_trade_type, subset=['trade_type']
        )
        
        st.dataframe(styled_df, use_container_width=True)
        
        # 거래 차트
        if len(trades_df) > 1:
            st.subheader("📈 거래 이력 차트")
            
            fig = go.Figure()
            
            buy_trades = trades_df[trades_df['trade_type'] == 'buy']
            sell_trades = trades_df[trades_df['trade_type'] == 'sell']
            
            if not buy_trades.empty:
                fig.add_trace(go.Scatter(
                    x=buy_trades['timestamp'],
                    y=buy_trades['price'],
                    mode='markers',
                    name='매수',
                    marker=dict(color='green', size=10, symbol='triangle-up')
                ))
            
            if not sell_trades.empty:
                fig.add_trace(go.Scatter(
                    x=sell_trades['timestamp'],
                    y=sell_trades['price'],
                    mode='markers',
                    name='매도',
                    marker=dict(color='red', size=10, symbol='triangle-down')
                ))
            
            fig.update_layout(
                title="거래 포인트",
                yaxis_title="가격 (KRW)",
                xaxis_title="시간",
                template="plotly_dark",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("거래 내역이 없습니다.")

def render_portfolio():
    """포트폴리오 페이지"""
    st.markdown('<h1 class="main-header">📊 포트폴리오 분석</h1>', unsafe_allow_html=True)
    
    db_data = load_database_data()
    
    # 포트폴리오 히스토리
    if db_data['portfolio_history']:
        portfolio_df = pd.DataFrame(db_data['portfolio_history'])
        portfolio_df['date'] = pd.to_datetime(portfolio_df['date'])
        portfolio_df = portfolio_df.sort_values('date')
        
        st.subheader("📈 포트폴리오 가치 변화")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=portfolio_df['date'],
            y=portfolio_df['total_value'],
            mode='lines+markers',
            name='총 자산 가치',
            line=dict(color='orange', width=3)
        ))
        
        fig.update_layout(
            title="포트폴리오 가치 추이",
            yaxis_title="가치 (KRW)",
            xaxis_title="날짜",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 수익률 차트
        if 'profit_loss_percent' in portfolio_df.columns:
            st.subheader("📊 수익률 변화")
            
            fig_profit = go.Figure()
            
            colors = ['green' if x >= 0 else 'red' for x in portfolio_df['profit_loss_percent']]
            
            fig_profit.add_trace(go.Bar(
                x=portfolio_df['date'],
                y=portfolio_df['profit_loss_percent'],
                name='수익률 (%)',
                marker_color=colors
            ))
            
            fig_profit.add_hline(y=0, line_dash="dash", line_color="white")
            
            fig_profit.update_layout(
                title="일별 수익률",
                yaxis_title="수익률 (%)",
                xaxis_title="날짜",
                template="plotly_dark",
                height=300
            )
            
            st.plotly_chart(fig_profit, use_container_width=True)
        
        # 포트폴리오 구성
        st.subheader("🥧 현재 포트폴리오 구성")
        
        if not portfolio_df.empty:
            latest = portfolio_df.iloc[-1]
            
            col1, col2 = st.columns(2)
            
            with col1:
                krw_balance = latest['krw_balance']
                btc_balance = latest['btc_balance']
                
                # 현재 비트코인 가격으로 BTC 가치 계산
                try:
                    current_btc_price = pyupbit.get_current_price("KRW-BTC")
                    btc_value = btc_balance * current_btc_price
                    total_value = krw_balance + btc_value
                    
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=['KRW', 'BTC'],
                        values=[krw_balance, btc_value],
                        hole=0.3,
                        marker_colors=['#FF6B35', '#FFA500']
                    )])
                    
                    fig_pie.update_layout(
                        title="자산 구성 비율",
                        template="plotly_dark",
                        height=300
                    )
                    
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                except Exception as e:
                    st.error(f"포트폴리오 구성 차트 생성 실패: {e}")
            
            with col2:
                st.metric("KRW 잔고", f"₩{krw_balance:,.0f}")
                st.metric("BTC 잔고", f"{btc_balance:.8f} BTC")
                if 'total_value' in locals():
                    st.metric("총 자산 가치", f"₩{total_value:,.0f}")
    
    else:
        st.info("포트폴리오 데이터가 없습니다.")

def render_ai_reflections():
    """AI 반성 일지 페이지"""
    st.markdown('<h1 class="main-header">🧠 AI 반성 일지</h1>', unsafe_allow_html=True)
    
    db_data = load_database_data()
    
    if db_data['recent_reflections']:
        st.subheader("📝 최근 AI 자기반성 내용")
        
        for i, reflection in enumerate(db_data['recent_reflections'][:5]):
            with st.expander(f"🤖 반성 {i+1}: {reflection.get('reflection_date', 'Unknown')}"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**분석 기간:**")
                    st.write(f"{reflection.get('analysis_period_start', '')} ~ {reflection.get('analysis_period_end', '')}")
                    
                    st.write("**거래 성과:**")
                    st.write(f"- 총 거래: {reflection.get('total_trades_analyzed', 0)}회")
                    st.write(f"- 성공: {reflection.get('successful_trades', 0)}회")
                    st.write(f"- 실패: {reflection.get('failed_trades', 0)}회")
                    st.write(f"- 승률: {reflection.get('win_rate', 0):.1f}%")
                
                with col2:
                    profit_loss = reflection.get('total_profit_loss', 0)
                    if profit_loss > 0:
                        st.success(f"**수익:** ₩{profit_loss:,.0f}")
                    elif profit_loss < 0:
                        st.error(f"**손실:** ₩{profit_loss:,.0f}")
                    else:
                        st.info("**손익:** ₩0")
                
                st.write("**AI 반성 내용:**")
                reflection_content = reflection.get('reflection_content', '반성 내용 없음')
                st.write(reflection_content)
                
                if reflection.get('lessons_learned'):
                    st.write("**학습한 교훈:**")
                    st.write(reflection.get('lessons_learned'))
                
                if reflection.get('improvement_suggestions'):
                    st.write("**개선 제안:**")
                    st.write(reflection.get('improvement_suggestions'))
    
    else:
        st.info("AI 반성 일지가 없습니다.")
    
    st.divider()
    
    # 전략 성과 분석 (DB 데이터 기반으로 간단히 구현)
    st.subheader("🎯 전략 성과 분석 (DB 기록 기준)")
    
    try:
        # DB에서 과열장/저점 관련 로그 분석
        recent_logs = db_data['recent_logs']
        
        overheated_count = 0
        bottom_count = 0
        buy_decisions = 0
        sell_decisions = 0
        
        for log in recent_logs[-30:]:  # 최근 30개 로그 분석
            try:
                market_data_json = json.loads(log.get('market_data_json', '{}'))
                advanced_analysis = market_data_json.get('advanced_strategy_analysis', {})
                
                if advanced_analysis.get('overheated_analysis', {}).get('overheated_level') != 'NONE':
                    overheated_count += 1
                    
                if advanced_analysis.get('bottom_buying_analysis', {}).get('bottom_level') != 'NONE':
                    bottom_count += 1
                    
            except:
                pass
            
            if log.get('ai_decision') == 'BUY':
                buy_decisions += 1
            elif log.get('ai_decision') == 'SELL':
                sell_decisions += 1
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("과열장 신호 횟수", f"{overheated_count}회", delta="최근 30회 분석")
        
        with col2:
            st.metric("저점 신호 횟수", f"{bottom_count}회", delta="최근 30회 분석")
        
        with col3:
            st.metric("매수 결정", f"{buy_decisions}회", delta="최근 30회 분석")
        
        with col4:
            st.metric("매도 결정", f"{sell_decisions}회", delta="최근 30회 분석")
        
        # 결정 분포 차트
        if buy_decisions + sell_decisions > 0:
            st.subheader("📊 AI 결정 분포")
            
            decisions = ['BUY', 'SELL', 'HOLD']
            counts = [buy_decisions, sell_decisions, len(recent_logs[-30:]) - buy_decisions - sell_decisions]
            
            fig = go.Figure(data=[go.Pie(
                labels=decisions,
                values=counts,
                hole=0.3,
                marker_colors=['#00D084', '#FF4757', '#FFA500']
            )])
            
            fig.update_layout(
                title="최근 30회 분석 결과",
                template="plotly_dark",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"전략 성과 분석 실패: {e}")

def render_analysis_logs():
    """분석 로그 페이지"""
    st.markdown('<h1 class="main-header">📋 AI 분석 로그</h1>', unsafe_allow_html=True)
    
    db_data = load_database_data()
    
    if db_data['recent_logs']:
        st.subheader("🤖 최근 AI 분석 결과")
        
        # 필터 옵션
        col1, col2 = st.columns(2)
        
        with col1:
            decision_filter = st.selectbox(
                "AI 결정 필터",
                options=['전체', 'BUY', 'SELL', 'HOLD'],
                index=0
            )
        
        with col2:
            show_count = st.slider("표시할 로그 수", min_value=5, max_value=50, value=20)
        
        # 로그 데이터 처리
        logs_df = pd.DataFrame(db_data['recent_logs'][:show_count])
        
        if decision_filter != '전체':
            logs_df = logs_df[logs_df['ai_decision'] == decision_filter]
        
        # 로그 표시
        for _, log in logs_df.iterrows():
            with st.expander(f"🕐 {log.get('timestamp', 'Unknown')} | {log.get('ai_decision', 'UNKNOWN')} | {log.get('ai_confidence', 'UNKNOWN')}"):
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**AI 분석 결과:**")
                    st.write(f"- 결정: **{log.get('ai_decision', 'UNKNOWN')}**")
                    st.write(f"- 신뢰도: **{log.get('ai_confidence', 'UNKNOWN')}**")
                    
                    reason = log.get('ai_reason', '분석 근거 없음')
                    st.write("**분석 근거:**")
                    st.write(reason)
                    
                    # 상세 AI 분석 정보 표시
                    try:
                        ai_analysis_json = log.get('ai_analysis_full_json', '{}')
                        if ai_analysis_json and ai_analysis_json != '{}':
                            ai_analysis = json.loads(ai_analysis_json)
                            
                            # 기술적 지표
                            if 'technical_indicators' in ai_analysis:
                                indicators = ai_analysis['technical_indicators']
                                st.write("**📊 기술적 지표:**")
                                
                                if 'rsi' in indicators:
                                    rsi_val = indicators['rsi']
                                    rsi_status = "과매수" if rsi_val > 70 else "과매도" if rsi_val < 30 else "중립"
                                    st.write(f"- RSI: **{rsi_val:.1f}** ({rsi_status})")
                                
                                if 'trend' in indicators:
                                    st.write(f"- 트렌드: **{indicators['trend']}**")
                                
                                if 'sma_5' in indicators and 'sma_20' in indicators:
                                    st.write(f"- SMA5: **{indicators['sma_5']:,.0f}** / SMA20: **{indicators['sma_20']:,.0f}**")
                            
                            # 시장 감정 및 위험도
                            sentiment = ai_analysis.get('market_sentiment', '')
                            risk_level = ai_analysis.get('risk_level', '')
                            
                            if sentiment or risk_level:
                                st.write("**🎯 시장 분석:**")
                                if sentiment:
                                    st.write(f"- 시장 감정: **{sentiment}**")
                                if risk_level:
                                    st.write(f"- 위험도: **{risk_level}**")
                                    
                    except Exception as e:
                        st.caption("상세 분석 정보 파싱 실패")
                
                with col2:
                    st.write("**시장 정보:**")
                    st.write(f"- 가격: ₩{log.get('current_price', 0):,.0f}")
                    st.write(f"- KRW 잔고: ₩{log.get('krw_balance', 0):,.0f}")
                    st.write(f"- BTC 잔고: {log.get('btc_balance', 0):.8f}")
                    st.write(f"- 총 자산: ₩{log.get('total_portfolio_value', 0):,.0f}")
                
                # 고급 전략 분석 결과 (있는 경우)
                try:
                    market_data_json = json.loads(log.get('market_data_json', '{}'))
                    advanced_analysis = market_data_json.get('advanced_strategy_analysis', {})
                    
                    if advanced_analysis:
                        st.write("**🎯 고급 전략 분석:**")
                        
                        overheated = advanced_analysis.get('overheated_analysis', {})
                        bottom = advanced_analysis.get('bottom_buying_analysis', {})
                        
                        col3, col4 = st.columns(2)
                        
                        with col3:
                            st.write(f"- 과열장 레벨: **{overheated.get('overheated_level', 'NONE')}**")
                            st.write(f"- 과열장 신호: {overheated.get('total_signals', 0)}개")
                        
                        with col4:
                            st.write(f"- 저점 레벨: **{bottom.get('bottom_level', 'NONE')}**")
                            st.write(f"- 저점 신호: {bottom.get('total_signals', 0)}개")
                
                except:
                    pass
    
    else:
        st.info("분석 로그가 없습니다.")

# 메인 앱
def main():
    """메인 애플리케이션"""
    
    # 사이드바 네비게이션
    st.sidebar.title("🚀 비트코인 매매 대시보드")
    st.sidebar.markdown("---")
    st.sidebar.info("📌 이 대시보드는 매매 기록 분석 전용입니다")
    
    # 페이지 선택
    pages = {
        "🏠 대시보드": render_main_dashboard,
        "⚡ 실시간 분석": render_realtime_analysis,
        "💰 매매 기록": render_trading_history,
        "📊 포트폴리오": render_portfolio,
        "🧠 AI 반성 일지": render_ai_reflections,
        "📋 분석 로그": render_analysis_logs
    }
    
    selected_page = st.sidebar.selectbox("페이지 선택", list(pages.keys()))
    
    st.sidebar.markdown("---")
    
    # 시스템 상태
    st.sidebar.subheader("🔧 시스템 상태")
    
    try:
        # 데이터베이스 연결 테스트
        db = TradingDatabase("trading_enhanced.db")
        recent_logs = db.get_recent_logs(1)
        
        if recent_logs:
            st.sidebar.success("✅ 데이터베이스 연결됨")
            last_analysis = recent_logs[0].get('timestamp', 'Unknown')
            st.sidebar.caption(f"마지막 분석: {last_analysis}")
        else:
            st.sidebar.warning("⚠️ 분석 데이터 없음")
            
    except Exception as e:
        st.sidebar.error("❌ 데이터베이스 오류")
        st.sidebar.caption(str(e))
    
    try:
        # 시장 데이터 연결 테스트 (선택사항)
        current_price = pyupbit.get_current_price("KRW-BTC")
        if current_price:
            st.sidebar.success("✅ 시장 데이터 연결됨")
            st.sidebar.caption(f"현재 BTC: ₩{current_price:,.0f}")
        else:
            st.sidebar.warning("⚠️ 시장 데이터 연결 실패")
            
    except Exception as e:
        st.sidebar.warning("⚠️ 시장 데이터 오프라인")
        st.sidebar.caption("DB 데이터만 표시됩니다")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("💾 데이터베이스: trading_enhanced.db")
    st.sidebar.caption("📊 GitHub 업로드용 대시보드")
    st.sidebar.caption("🔗 실제 매매는 별도 시스템에서 진행")
    
    # 선택된 페이지 렌더링
    pages[selected_page]()

if __name__ == "__main__":
    main() 