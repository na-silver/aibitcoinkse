#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 AI 트레이딩 투자 결과 대시보드
Trading Results Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import TradingDatabase

# 페이지 설정
st.set_page_config(
    page_title="📊 AI Bitcoin Trading Dashboard",
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 전문적인 금융 대시보드 CSS 스타일링
st.markdown("""
<style>
    /* 전체 페이지 배경 */
    .main {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%);
        color: #ffffff;
    }
    
    /* 메인 헤더 - 프로페셔널 스타일 */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #1a2a3a 0%, #2a1a2a 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* 서브 헤더 */
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: #b0b0b0;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* 메트릭 카드 컨테이너 */
    .metric-container {
        background: linear-gradient(135deg, #2c2c2c 0%, #1e1e1e 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* 개별 메트릭 카드 */
    .metric-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        font-size: 14px;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    
    /* 성공 메트릭 (수익) */
    .success-card {
        border-left-color: #00d084;
        background: linear-gradient(135deg, #1a3d2e 0%, #0f2419 100%);
    }
    
    /* 위험 메트릭 (손실) */
    .danger-card {
        border-left-color: #ff4757;
        background: linear-gradient(135deg, #3d1a1a 0%, #241010 100%);
    }
    
    /* 정보 메트릭 */
    .info-card {
        border-left-color: #3742fa;
        background: linear-gradient(135deg, #1a1d3d 0%, #0f1024 100%);
    }
    
    /* 경고 메트릭 */
    .warning-card {
        border-left-color: #ffa502;
        background: linear-gradient(135deg, #3d2e1a 0%, #24190f 100%);
    }
    
    /* 섹션 헤더 */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #6a7a8a;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(106, 122, 138, 0.3);
    }
    
    /* 차트 컨테이너 */
    .chart-container {
        background: linear-gradient(135deg, #2c2c2c 0%, #1e1e1e 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* 스탯 박스 */
    .stat-box {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* 스탯 값 */
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #6a7a8a;
        margin-bottom: 0.5rem;
    }
    
    /* 스탯 라벨 */
    .stat-label {
        font-size: 0.9rem;
        color: #b0b0b0;
        font-weight: 400;
    }
    
    /* 탭 스타일 개선 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(135deg, #2c2c2c 0%, #1e1e1e 100%);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        color: #b0b0b0;
        border: 1px solid rgba(255,255,255,0.1);
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1a2a3a 0%, #2a1a2a 100%);
        color: #ffffff;
    }
    
    /* 데이터프레임 스타일 */
    .dataframe {
        background: linear-gradient(135deg, #2c2c2c 0%, #1e1e1e 100%);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* 익스팬더 스타일 */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* 사이드바 숨기기 */
    .css-1d391kg {
        display: none;
    }
    
    /* 푸터 숨기기 */
    .css-1lsmgbg {
        display: none;
    }
    
    /* Streamlit 메뉴 숨기기 */
    #MainMenu {
        visibility: hidden;
    }
    
    /* 워터마크 숨기기 */
    footer {
        visibility: hidden;
    }
    
    /* 헤더 숨기기 */
    header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_trading_data():
    """거래 데이터 로드"""
    try:
        # TradingDatabase 클래스 사용
        db = TradingDatabase("trading_enhanced.db")
        
        # 거래 내역 - 최근 1년간 데이터
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        trades_data = db.get_trades_by_date(start_date, end_date)
        trades_df = pd.DataFrame(trades_data)
        
        # 포트폴리오 히스토리
        portfolio_data = db.get_portfolio_history(100)
        portfolio_df = pd.DataFrame(portfolio_data)
        
        # AI 분석 로그
        ai_logs_data = db.get_recent_logs(50)
        ai_logs_df = pd.DataFrame(ai_logs_data)
        
        return {
            'trades': trades_df,
            'portfolio': portfolio_df,
            'ai_logs': ai_logs_df,
            'status': 'success'
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def calculate_performance_metrics(trades_df):
    """성과 지표 계산"""
    if trades_df.empty:
        return {}
    
    # 기본 통계
    total_trades = len(trades_df)
    buy_trades = trades_df[trades_df['trade_type'] == 'buy']
    sell_trades = trades_df[trades_df['trade_type'] == 'sell']
    
    total_buy_value = buy_trades['total_value'].sum() if not buy_trades.empty else 0
    total_sell_value = sell_trades['total_value'].sum() if not sell_trades.empty else 0
    total_fees = trades_df['fee'].sum()
    
    # 현재 포트폴리오 가치 가져오기
    try:
        db = TradingDatabase("trading_enhanced.db")
        portfolio_data = db.get_portfolio_history(1)
        current_portfolio_value = portfolio_data[0]['total_value'] if portfolio_data else 0
    except:
        current_portfolio_value = 0
    
    # 수익률 계산 (개선된 로직)
    if total_buy_value > 0:
        if len(sell_trades) > 0:
            # 매도 거래가 있는 경우: 기존 로직 사용
            net_profit = total_sell_value - total_buy_value
            roi = (net_profit / total_buy_value * 100)
        else:
            # 매도 거래가 없는 경우: 현재 포트폴리오에서 투자한 BTC 가치 계산
            # 투자 수익률 = (현재 BTC 가치 + 잔여 KRW - 총 매수 금액) / 총 매수 금액 * 100
            try:
                portfolio_data = db.get_portfolio_history(1)
                if portfolio_data:
                    current_krw = portfolio_data[0]['krw_balance']
                    current_btc = portfolio_data[0]['btc_balance']
                    current_btc_price = portfolio_data[0].get('btc_avg_price', 0)
                    
                    # 현재 BTC 가치 + 잔여 KRW = 실제 자산 가치
                    current_asset_value = (current_btc * current_btc_price) + current_krw
                    net_profit = current_asset_value - total_buy_value
                    roi = (net_profit / total_buy_value * 100)
                else:
                    # 백업 계산
                    net_profit = current_portfolio_value - total_buy_value
                    roi = (net_profit / total_buy_value * 100)
            except:
                # 백업 계산: 현재 가치 vs 매수 금액
                net_profit = current_portfolio_value - total_buy_value
                roi = (net_profit / total_buy_value * 100)
    else:
        net_profit = 0
        roi = 0
    
    return {
        'total_trades': total_trades,
        'buy_count': len(buy_trades),
        'sell_count': len(sell_trades),
        'total_buy_value': total_buy_value,
        'total_sell_value': total_sell_value,
        'total_fees': total_fees,
        'net_profit': net_profit,
        'roi': roi,
        'current_portfolio_value': current_portfolio_value
    }

def render_performance_overview(metrics):
    """성과 개요"""
    # 프로페셔널 헤더
    st.markdown('''
    <div class="metric-container">
        <h2 class="section-header">📈 투자 성과 개요</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    # 메트릭 카드들을 전문적인 스타일로 배치
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        profit_trend = "📈" if metrics['net_profit'] >= 0 else "📉"
        st.markdown(f'''
        <div class="stat-box info-card">
            <div class="stat-value">{metrics['total_trades']}</div>
            <div class="stat-label">총 거래 횟수</div>
            <div style="margin-top: 0.5rem; color: #b0b0b0; font-size: 0.8rem;">
                매수 {metrics['buy_count']} | 매도 {metrics['sell_count']}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        profit_style = "success-card" if metrics['net_profit'] >= 0 else "danger-card"
        profit_icon = "💰" if metrics['net_profit'] >= 0 else "💸"
        st.markdown(f'''
        <div class="stat-box {profit_style}">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">{profit_icon}</div>
            <div class="stat-value">₩{metrics['net_profit']:,.0f}</div>
            <div class="stat-label">순손익</div>
            <div style="margin-top: 0.5rem; color: {'#00d084' if metrics['net_profit'] >= 0 else '#ff4757'}; font-weight: 600; font-size: 0.9rem;">
                {metrics['roi']:+.2f}%
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stat-box warning-card">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">🏦</div>
            <div class="stat-value">₩{metrics.get('current_portfolio_value', 0):,.0f}</div>
            <div class="stat-label">현재 포트폴리오</div>
            <div style="margin-top: 0.5rem; color: #b0b0b0; font-size: 0.8rem;">
                투자금액 ₩{metrics['total_buy_value']:,.0f}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="stat-box metric-card">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">💳</div>
            <div class="stat-value">₩{metrics['total_fees']:,.0f}</div>
            <div class="stat-label">총 수수료</div>
            <div style="margin-top: 0.5rem; color: #b0b0b0; font-size: 0.8rem;">
                거래당 평균 ₩{metrics['total_fees']/max(1, metrics['total_trades']):,.0f}
            </div>
        </div>
        ''', unsafe_allow_html=True)

def render_trades_table(trades_df):
    """거래 내역 테이블"""
    st.markdown('''
    <div class="chart-container">
        <h2 class="section-header">📋 거래 내역</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if trades_df.empty:
        st.warning("거래 내역이 없습니다.")
        return
    
    # 데이터 전처리
    display_df = trades_df.copy()
    display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    display_df['price'] = display_df['price'].apply(lambda x: f"₩{x:,.0f}")
    display_df['amount'] = display_df['amount'].apply(lambda x: f"{x:.6f}")
    display_df['total_value'] = display_df['total_value'].apply(lambda x: f"₩{x:,.0f}")
    display_df['fee'] = display_df['fee'].apply(lambda x: f"₩{x:,.0f}")
    
    # 컬럼 선택 및 이름 변경
    display_df = display_df[['timestamp', 'trade_type', 'price', 'amount', 'total_value', 'fee', 'success']]
    display_df.columns = ['시간', '타입', '가격', '수량(BTC)', '총액', '수수료', '성공']
    
    st.dataframe(display_df, use_container_width=True, height=400)

def render_portfolio_chart(portfolio_df):
    """포트폴리오 변화 차트"""
    st.markdown('''
    <div class="chart-container">
        <h2 class="section-header">📊 포트폴리오 변화</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if portfolio_df.empty:
        st.warning("포트폴리오 히스토리가 없습니다.")
        return
    
    # 시간순 정렬 (date 컬럼 사용 - 오래된 것부터)
    portfolio_df = portfolio_df.sort_values('date')
    portfolio_df['date'] = pd.to_datetime(portfolio_df['date'])
    
    # 초기 투자 금액 설정 (가장 오래된 데이터)
    initial_investment = portfolio_df.iloc[0]['total_value'] if len(portfolio_df) > 0 else 1000000
    
    # 일별 손익 계산
    portfolio_df['daily_profit'] = portfolio_df['total_value'] - initial_investment
    portfolio_df['daily_roi'] = (portfolio_df['daily_profit'] / initial_investment * 100).round(2)
    
    # 차트 생성
    fig = go.Figure()
    
    # 총 자산 가치
    fig.add_trace(go.Scatter(
        x=portfolio_df['date'],
        y=portfolio_df['total_value'],
        mode='lines+markers',
        name='총 자산',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=6),
        hovertemplate='<b>총 자산</b><br>날짜: %{x}<br>가치: ₩%{y:,.0f}<extra></extra>'
    ))
    
    # KRW 잔고
    fig.add_trace(go.Scatter(
        x=portfolio_df['date'],
        y=portfolio_df['krw_balance'],
        mode='lines',
        name='KRW 잔고',
        line=dict(color='#00D084', width=2),
        hovertemplate='<b>KRW 잔고</b><br>날짜: %{x}<br>잔고: ₩%{y:,.0f}<extra></extra>'
    ))
    
    # BTC 가치 계산 (btc_balance * btc_avg_price)
    if 'btc_balance' in portfolio_df.columns and 'btc_avg_price' in portfolio_df.columns:
        portfolio_df['btc_value_krw'] = portfolio_df['btc_balance'] * portfolio_df['btc_avg_price']
        fig.add_trace(go.Scatter(
            x=portfolio_df['date'],
            y=portfolio_df['btc_value_krw'],
            mode='lines',
            name='BTC 가치',
            line=dict(color='#FFA500', width=2)
        ))
    
    fig.update_layout(
        title={
            'text': "포트폴리오 가치 변화",
            'x': 0.5,
            'font': {'size': 18, 'color': '#667eea', 'family': 'Arial Black'}
        },
        xaxis_title="날짜",
        yaxis_title="가치 (KRW)",
        template="plotly_dark",
        height=500,
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        legend={
            'bgcolor': 'rgba(0,0,0,0.5)',
            'bordercolor': 'rgba(255,255,255,0.1)',
            'borderwidth': 1
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_profit_loss_chart(portfolio_df):
    """손익 차트"""
    st.markdown('''
    <div class="chart-container">
        <h2 class="section-header">💰 손익 분석</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if portfolio_df.empty:
        st.warning("포트폴리오 히스토리가 없습니다.")
        return
    
    # 시간순 정렬 (오래된 것부터)
    portfolio_df = portfolio_df.sort_values('date')
    portfolio_df['date'] = pd.to_datetime(portfolio_df['date'])
    
    # 초기 투자 금액 설정 (가장 오래된 데이터)
    initial_investment = portfolio_df.iloc[0]['total_value'] if len(portfolio_df) > 0 else 1000000
    
    # 손익 계산
    portfolio_df['daily_profit'] = portfolio_df['total_value'] - initial_investment
    portfolio_df['daily_roi'] = (portfolio_df['daily_profit'] / initial_investment * 100).round(2)
    
    # 색상 조건 (수익/손실에 따른 색상 변화)
    colors = ['#00D084' if profit >= 0 else '#FF4757' for profit in portfolio_df['daily_profit']]
    
    # 손익 통계 표시
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        max_profit = portfolio_df['daily_profit'].max()
        st.markdown(f'''
        <div class="stat-box success-card">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">📈</div>
            <div class="stat-value">₩{max_profit:,.0f}</div>
            <div class="stat-label">최대 수익</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        min_profit = portfolio_df['daily_profit'].min()
        st.markdown(f'''
        <div class="stat-box danger-card">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">📉</div>
            <div class="stat-value">₩{min_profit:,.0f}</div>
            <div class="stat-label">최대 손실</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        avg_profit = portfolio_df['daily_profit'].mean()
        avg_style = "success-card" if avg_profit >= 0 else "danger-card"
        avg_icon = "⚖️"
        st.markdown(f'''
        <div class="stat-box {avg_style}">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">{avg_icon}</div>
            <div class="stat-value">₩{avg_profit:,.0f}</div>
            <div class="stat-label">평균 손익</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # 수익일 비율 제거 - 4번째 컬럼 공백으로 유지
    with col4:
        st.markdown('')  # 빈 공간
    
    # 손익 막대 차트
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=portfolio_df['date'],
        y=portfolio_df['daily_profit'],
        name='일별 손익',
        marker_color=colors,
        hovertemplate='<b>일별 손익</b><br>날짜: %{x}<br>손익: ₩%{y:,.0f}<br>수익률: %{customdata:.2f}%<extra></extra>',
        customdata=portfolio_df['daily_roi']
    ))
    
    # 0선 표시
    fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
    
    fig.update_layout(
        title={
            'text': "일별 손익 분포",
            'x': 0.5,
            'font': {'size': 16, 'color': '#667eea', 'family': 'Arial Black'}
        },
        xaxis_title="날짜",
        yaxis_title="손익 (KRW)",
        template="plotly_dark",
        height=400,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 누적 손익 차트
    st.markdown('''
    <div style="margin-top: 2rem;">
        <h3 class="section-header">📈 누적 손익 추이</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=portfolio_df['date'],
        y=portfolio_df['daily_profit'],
        mode='lines+markers',
        name='누적 손익',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=6),
        fill='tonexty',
        fillcolor='rgba(255, 107, 53, 0.1)',
        hovertemplate='<b>누적 손익</b><br>날짜: %{x}<br>손익: ₩%{y:,.0f}<br>수익률: %{customdata:.2f}%<extra></extra>',
        customdata=portfolio_df['daily_roi']
    ))
    
    # 0선 표시
    fig2.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
    
    fig2.update_layout(
        title={
            'text': "누적 손익 추이",
            'x': 0.5,
            'font': {'size': 16, 'color': '#667eea', 'family': 'Arial Black'}
        },
        xaxis_title="날짜",
        yaxis_title="누적 손익 (KRW)",
        template="plotly_dark",
        height=400,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'},
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'}
    )
    
    st.plotly_chart(fig2, use_container_width=True)

def safe_float(value, default=0):
    """안전한 float 변환"""
    try:
        if value is None or value == 'N/A':
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def clean_html_tags(text):
    """HTML 태그 제거 및 텍스트 정리"""
    import re
    if not text:
        return "분석 내용이 없습니다."
    
    # HTML 태그 제거
    clean_text = re.sub(r'<[^>]+>', '', str(text))
    
    # HTML 엔티티 변환
    clean_text = clean_text.replace('&nbsp;', ' ')
    clean_text = clean_text.replace('&lt;', '<')
    clean_text = clean_text.replace('&gt;', '>')
    clean_text = clean_text.replace('&amp;', '&')
    
    # 과도한 공백 정리
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = clean_text.strip()
    
    # 길이 제한 (너무 길면 잘라내기)
    if len(clean_text) > 2000:
        clean_text = clean_text[:2000] + "...\n\n[내용이 너무 길어 일부만 표시됩니다]"
    
    return clean_text if clean_text else "분석 내용이 없습니다."

def parse_analysis_sections(text):
    """AI 분석 내용을 섹션별로 파싱"""
    import re
    
    if not text or len(text.strip()) < 50:
        return []
    
    # 섹션 패턴과 해당 아이콘/제목 매핑
    section_patterns = [
        {
            'pattern': r'(기술적 분석.*?TECHNICAL ANALYSIS.*?):(.*?)(?=(?:시장 심리|뉴스 감정|유튜브|유동성|리스크|포지션|실행|$))',
            'icon': '📊',
            'title': '기술적 분석'
        },
        {
            'pattern': r'(시장 심리.*?SENTIMENT ANALYSIS.*?):(.*?)(?=(?:뉴스 감정|유튜브|유동성|리스크|포지션|실행|기술적|$))',
            'icon': '😊',
            'title': '시장 심리'
        },
        {
            'pattern': r'(뉴스 감정.*?NEWS SENTIMENT.*?):(.*?)(?=(?:유튜브|유동성|리스크|포지션|실행|기술적|시장|$))',
            'icon': '📰',
            'title': '뉴스 분석'
        },
        {
            'pattern': r'(유튜브.*?YOUTUBE.*?ANALYSIS.*?):(.*?)(?=(?:유동성|리스크|포지션|실행|기술적|시장|뉴스|$))',
            'icon': '📱',
            'title': '소셜 분석'
        },
        {
            'pattern': r'(유동성.*?LIQUIDITY.*?):(.*?)(?=(?:리스크|포지션|실행|기술적|시장|뉴스|유튜브|$))',
            'icon': '💧',
            'title': '유동성 분석'
        },
        {
            'pattern': r'(리스크.*?RISK.*?ASSESSMENT.*?):(.*?)(?=(?:포지션|실행|기술적|시장|뉴스|유튜브|유동성|$))',
            'icon': '⚖️',
            'title': '리스크 평가'
        },
        {
            'pattern': r'(포지션.*?POSITION.*?STRATEGY.*?):(.*?)(?=(?:실행|기술적|시장|뉴스|유튜브|유동성|리스크|$))',
            'icon': '📈',
            'title': '포지션 전략'
        },
        {
            'pattern': r'(실행.*?ACTIONABLE.*?):(.*?)(?=(?:기술적|시장|뉴스|유튜브|유동성|리스크|포지션|$))',
            'icon': '🎯',
            'title': '실행 전략'
        }
    ]
    
    sections = []
    
    for section_info in section_patterns:
        matches = re.finditer(section_info['pattern'], text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            content = match.group(2).strip()
            if content and len(content) > 10:
                # 내용을 정리하고 읽기 쉽게 포맷
                content = re.sub(r'\s+', ' ', content)
                content = content.replace('|', '\n• ')
                
                # 기술적 용어들 사이에 줄바꿈 추가 (가독성 개선)
                content = content.replace('RSI:', '\n• RSI: ')
                content = content.replace('MACD:', '\n• MACD: ')
                content = content.replace('일봉:', '\n• 일봉: ')
                content = content.replace('시간봉:', '\n• 시간봉: ')
                content = content.replace('다이버전스:', '\n• 다이버전스: ')
                content = content.replace('볼린저밴드:', '\n• 볼린저밴드: ')
                content = content.replace('이동평균선:', '\n• 이동평균선: ')
                content = content.replace('스토캐스틱:', '\n• 스토캐스틱: ')
                content = content.replace('거래량:', '\n• 거래량: ')
                content = content.replace('지지선:', '\n• 지지선: ')
                content = content.replace('저항선:', '\n• 저항선: ')
                content = content.replace('트렌드:', '\n• 트렌드: ')
                content = content.replace('오실레이터:', '\n• 오실레이터: ')
                content = content.replace('황금십자:', '\n• 황금십자: ')
                content = content.replace('죽음의십자:', '\n• 죽음의십자: ')
                
                # 내용 정리 (길이 제한 없이 전체 내용 표시)
                
                sections.append({
                    'icon': section_info['icon'],
                    'title': section_info['title'],
                    'content': content
                })
    
    # 섹션이 없으면 전체 텍스트를 요약해서 반환
    if not sections and text.strip():
        # 텍스트를 4개 섹션으로 나누기
        parts = text.split('. ')
        if len(parts) > 8:
            section_size = len(parts) // 4
            for i in range(4):
                start_idx = i * section_size
                end_idx = start_idx + section_size if i < 3 else len(parts)
                section_text = '. '.join(parts[start_idx:end_idx])
                
                if section_text.strip():
                    sections.append({
                        'icon': ['📊', '💡', '⚡', '🎯'][i],
                        'title': ['기술 분석', '시장 동향', '전략 요소', '실행 계획'][i],
                        'content': section_text[:200] + '...' if len(section_text) > 200 else section_text
                    })
    
    return sections

def render_ai_analysis_detailed(ai_logs_df):
    """AI 분석 상세"""
    st.markdown('''
    <div class="chart-container">
        <h2 class="section-header">🧠 AI 분석 상세</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if ai_logs_df.empty:
        st.warning("AI 분석 데이터가 없습니다.")
        return
    
    # AI 분석 통계 대시보드
    st.markdown('<h3 class="section-header">📊 AI 분석 통계</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_analyses = len(ai_logs_df)
    
    with col1:
        st.markdown(f'''
        <div class="stat-box info-card">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">🔍</div>
            <div class="stat-value">{total_analyses}</div>
            <div class="stat-label">총 분석 횟수</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # 결정 분포
    if 'ai_decision' in ai_logs_df.columns:
        buy_count = len(ai_logs_df[ai_logs_df['ai_decision'] == 'BUY'])
        sell_count = len(ai_logs_df[ai_logs_df['ai_decision'] == 'SELL'])
        hold_count = len(ai_logs_df[ai_logs_df['ai_decision'] == 'HOLD'])
        
        with col2:
            st.markdown(f'''
            <div class="stat-box success-card">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">🟢</div>
                <div class="stat-value">{buy_count}</div>
                <div class="stat-label">매수 결정</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="stat-box danger-card">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">🔴</div>
                <div class="stat-value">{sell_count}</div>
                <div class="stat-label">매도 결정</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="stat-box warning-card">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">🟡</div>
                <div class="stat-value">{hold_count}</div>
                <div class="stat-label">홀드 결정</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 고급 필터 옵션
    st.markdown('<h3 class="section-header">🔍 분석 필터</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        decision_filter = st.selectbox(
            "AI 결정 필터",
            ['전체'] + list(ai_logs_df['ai_decision'].unique()) if 'ai_decision' in ai_logs_df.columns else ['전체']
        )
    
    with col2:
        if 'ai_confidence' in ai_logs_df.columns:
            unique_confidences = sorted(list(ai_logs_df['ai_confidence'].unique()))
            confidence_filter = st.selectbox(
                "신뢰도 필터", 
                ['전체'] + unique_confidences
            )
        else:
            confidence_filter = st.selectbox(
                "신뢰도 필터", 
                ['전체']
            )
    
    with col3:
        # 날짜 필터 (최근 N일)
        date_filter = st.selectbox(
            "기간 필터",
            ['전체', '최근 1일', '최근 3일', '최근 7일']
        )
    
    # 데이터 필터링
    filtered_df = ai_logs_df.copy()
    
    if decision_filter != '전체':
        filtered_df = filtered_df[filtered_df['ai_decision'] == decision_filter]
    if confidence_filter != '전체':
        filtered_df = filtered_df[filtered_df['ai_confidence'] == confidence_filter]
    
    if date_filter != '전체':
        days_map = {'최근 1일': 1, '최근 3일': 3, '최근 7일': 7}
        if date_filter in days_map:
            cutoff_date = datetime.now() - timedelta(days=days_map[date_filter])
            filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
            filtered_df = filtered_df[filtered_df['timestamp'] >= cutoff_date]
    
    st.markdown("---")
    
    # AI 분석 타임라인
    st.markdown('<h3 class="section-header">⏰ AI 분석 타임라인</h3>', unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.info("필터 조건에 맞는 분석 결과가 없습니다.")
        return
    
    # 분석 결과를 카드 형태로 표시
    for i, row in filtered_df.head(10).iterrows():
        timestamp = pd.to_datetime(row.get('timestamp', '')).strftime('%Y-%m-%d %H:%M:%S') if row.get('timestamp') else 'N/A'
        decision = row.get('ai_decision', 'N/A')
        confidence = row.get('ai_confidence', 'N/A')
        reason = row.get('ai_reason', '분석 상세 정보가 없습니다.')
        
        # HTML 태그 직접 제거
        import re
        clean_reason = str(reason)
        clean_reason = re.sub(r'<[^>]+>', '', clean_reason)  # HTML 태그 제거
        clean_reason = clean_reason.replace('&nbsp;', ' ')    # HTML 엔티티 변환
        clean_reason = clean_reason.replace('&lt;', '<')
        clean_reason = clean_reason.replace('&gt;', '>')
        clean_reason = clean_reason.replace('&amp;', '&')
        clean_reason = re.sub(r'\s+', ' ', clean_reason)      # 공백 정리
        clean_reason = clean_reason.strip()
        
        # 길이 제한
        if len(clean_reason) > 1500:
            clean_reason = clean_reason[:1500] + "...\n\n[내용이 너무 길어 일부만 표시됩니다]"
        
        if not clean_reason:
            clean_reason = "분석 내용이 없습니다."
        
        # 결정에 따른 카드 색상
        if decision == 'BUY':
            card_color = "success-card"
            decision_icon = "🟢"
        elif decision == 'SELL':
            card_color = "danger-card" 
            decision_icon = "🔴"
        elif decision == 'HOLD':
            card_color = "warning-card"
            decision_icon = "🟡"
        else:
            card_color = "info-card"
            decision_icon = "⚪"
        
        # 신뢰도에 따른 신뢰도 바
        try:
            if confidence == 'N/A':
                conf_value = 0
            elif isinstance(confidence, str):
                # 문자열에서 숫자 추출 시도
                try:
                    conf_value = float(confidence)
                except ValueError:
                    # "MEDIUM", "HIGH" 같은 형태면 매핑
                    conf_upper = confidence.upper()
                    confidence_mapping = {
                        'LOW': 0.3,
                        'MEDIUM': 0.6, 
                        'HIGH': 0.9,
                        'VERY_HIGH': 1.0
                    }
                    conf_value = confidence_mapping.get(conf_upper, 0.5)
            else:
                conf_value = float(confidence)
            
            conf_color = "#00d084" if conf_value >= 0.7 else "#ffa502" if conf_value >= 0.5 else "#ff4757"
            conf_width = conf_value * 100
        except:
            conf_value = 0
            conf_color = "#666"
            conf_width = 0
        
        # HTML 대신 Streamlit 네이티브 컴포넌트 사용
        with st.container():
            st.markdown(f"### {decision_icon} AI 분석 #{i+1}")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"📅 **시간**: {timestamp}")
                st.write(f"🎯 **결정**: {decision}")
                st.write(f"🔒 **신뢰도**: {confidence}")
            
            with col2:
                # 신뢰도 바 표시
                if conf_value > 0:
                    st.progress(conf_value)
                    st.caption(f"신뢰도: {conf_value:.1%}")
            
            st.markdown("**🧠 AI 분석 내용**")
            
            # AI 분석 내용을 섹션별로 파싱
            analysis_sections = parse_analysis_sections(clean_reason)
            
            # 분석 섹션들을 카드 형태로 표시
            if analysis_sections:
                # 4열로 배치하여 작은 카드들로 한 행에 더 많이 표시
                for i in range(0, len(analysis_sections), 4):
                    cols = st.columns(4)
                    
                    for j in range(4):
                        if i + j < len(analysis_sections):
                            section = analysis_sections[i + j]
                            with cols[j]:
                                # 작은 카드 스타일로 표시
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, #1a2a3a 0%, #2a1a2a 100%);
                                    padding: 20px;
                                    border-radius: 15px;
                                    margin: 10px 0;
                                    color: white;
                                    font-size: 14px;
                                    min-height: 200px;
                                    max-height: 600px;
                                    overflow-y: auto;
                                    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
                                    border: 1px solid rgba(255,255,255,0.05);
                                ">
                                    <div style="font-weight: bold; font-size: 17px; margin-bottom: 12px; color: #FFE66D;">
                                        {section['icon']} {section['title']}
                                    </div>
                                    <div style="font-size: 14px; line-height: 1.5; white-space: pre-line;">
                                        {section['content']}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
            else:
                # 섹션 파싱이 실패하면 원본 텍스트 표시
                # 전체 분석 내용에서도 용어들 사이에 줄바꿈 추가
                formatted_reason = clean_reason
                formatted_reason = formatted_reason.replace('RSI:', '\n• RSI: ')
                formatted_reason = formatted_reason.replace('MACD:', '\n• MACD: ')
                formatted_reason = formatted_reason.replace('일봉:', '\n• 일봉: ')
                formatted_reason = formatted_reason.replace('시간봉:', '\n• 시간봉: ')
                formatted_reason = formatted_reason.replace('다이버전스:', '\n• 다이버전스: ')
                formatted_reason = formatted_reason.replace('볼린저밴드:', '\n• 볼린저밴드: ')
                formatted_reason = formatted_reason.replace('이동평균선:', '\n• 이동평균선: ')
                formatted_reason = formatted_reason.replace('스토캐스틱:', '\n• 스토캐스틱: ')
                formatted_reason = formatted_reason.replace('거래량:', '\n• 거래량: ')
                formatted_reason = formatted_reason.replace('지지선:', '\n• 지지선: ')
                formatted_reason = formatted_reason.replace('저항선:', '\n• 저항선: ')
                formatted_reason = formatted_reason.replace('트렌드:', '\n• 트렌드: ')
                formatted_reason = formatted_reason.replace('오실레이터:', '\n• 오실레이터: ')
                formatted_reason = formatted_reason.replace('황금십자:', '\n• 황금십자: ')
                formatted_reason = formatted_reason.replace('죽음의십자:', '\n• 죽음의십자: ')
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #1a2a3a 0%, #2a1a2a 100%);
                    padding: 25px;
                    border-radius: 15px;
                    margin: 15px 0;
                    color: white;
                    font-size: 14px;
                    min-height: 200px;
                    max-height: 800px;
                    overflow-y: auto;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
                    border: 1px solid rgba(255,255,255,0.05);
                ">
                    <div style="font-weight: bold; font-size: 18px; margin-bottom: 15px; color: #FFE66D;">
                        📄 전체 분석 내용
                    </div>
                    <div style="font-size: 14px; line-height: 1.5; white-space: pre-line;">
                        {formatted_reason}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # 포트폴리오 정보
            st.caption(f"💰 BTC 가격: ₩{safe_float(row.get('current_price')):,.0f} | "
                      f"💵 KRW: ₩{safe_float(row.get('krw_balance')):,.0f} | "
                      f"🪙 BTC: {safe_float(row.get('btc_balance')):.6f}")
            
            st.divider()
    
    # 더 많은 분석 보기 버튼
    if len(filtered_df) > 10:
        st.info(f"총 {len(filtered_df)}개의 분석 중 최근 10개를 표시했습니다.")
    
    # 분석 인사이트
    st.markdown("---")
    st.markdown('<h3 class="section-header">💡 AI 분석 인사이트</h3>', unsafe_allow_html=True)
    
    if 'ai_confidence' in filtered_df.columns and len(filtered_df) > 0:
        # 신뢰도 분포 계산
        confidence_counts = filtered_df['ai_confidence'].value_counts()
        total_analyses = len(filtered_df)
        
        # 신뢰도 매핑 (숫자 변환용)
        confidence_mapping = {
            'LOW': 0.3,
            'MEDIUM': 0.6, 
            'HIGH': 0.9,
            'VERY_HIGH': 1.0
        }
        
        # 숫자로 변환 가능한 신뢰도만 추출
        numeric_confidences = []
        for conf in filtered_df['ai_confidence']:
            if isinstance(conf, str):
                # 문자열에서 숫자 추출 시도
                try:
                    # "0.85" 같은 형태인지 확인
                    float_val = float(conf)
                    numeric_confidences.append(float_val)
                except ValueError:
                    # "MEDIUM", "HIGH" 같은 형태면 매핑
                    conf_upper = conf.upper()
                    if conf_upper in confidence_mapping:
                        numeric_confidences.append(confidence_mapping[conf_upper])
            elif isinstance(conf, (int, float)):
                numeric_confidences.append(float(conf))
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 가장 많은 신뢰도 레벨 표시
            most_common_confidence = confidence_counts.index[0] if len(confidence_counts) > 0 else 'N/A'
            most_common_count = confidence_counts.iloc[0] if len(confidence_counts) > 0 else 0
            
            st.markdown(f'''
            <div class="stat-box info-card">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                    <div style="font-size: 1.3rem; font-weight: bold;">{most_common_confidence}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">가장 많은 신뢰도 ({most_common_count}회)</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            # 숫자 신뢰도가 있으면 평균 계산, 없으면 총 분석 수 표시
            if numeric_confidences:
                avg_confidence = sum(numeric_confidences) / len(numeric_confidences)
                st.markdown(f'''
                <div class="stat-box success-card">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                        <div style="font-size: 1.3rem; font-weight: bold;">{avg_confidence:.3f}</div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">평균 신뢰도</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="stat-box success-card">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                        <div style="font-size: 1.3rem; font-weight: bold;">{total_analyses}</div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">총 분석 수</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info("신뢰도 분석 데이터가 없습니다.")


def render_ai_decision_chart(ai_logs_df):
    """AI 결정 분포 차트"""
    st.markdown('''
    <div class="chart-container">
        <h2 class="section-header">📈 AI 결정 분포</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if ai_logs_df.empty or 'ai_decision' not in ai_logs_df.columns:
        st.warning("AI 결정 데이터가 없습니다.")
        return
    
    # 결정 분포 계산
    decision_counts = ai_logs_df['ai_decision'].value_counts()
    
    # 파이 차트
    fig = go.Figure(data=[go.Pie(
        labels=decision_counts.index,
        values=decision_counts.values,
        hole=.3,
        marker_colors=['#FF6B35', '#00D084', '#FFA500']
    )])
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title={
            'text': "AI 결정 분포",
            'x': 0.5,
            'font': {'size': 16, 'color': '#667eea', 'family': 'Arial Black'}
        },
        template="plotly_dark",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    """메인 대시보드"""
    # 프로페셔널 헤더
    st.markdown('''
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="main-header">📊 AI Bitcoin Trading Dashboard</h1>
        <p class="sub-header">Advanced Investment Performance Analytics</p>
        <div style="margin: 1rem 0; padding: 1rem; background: linear-gradient(135deg, #2c2c2c 0%, #1e1e1e 100%); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
            <span style="color: #667eea; font-weight: 600;">Real-time Bitcoin Analysis & Trading Performance</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 데이터 로드
    data = load_trading_data()
    
    if data['status'] != 'success':
        st.error("❌ 데이터 로드 실패")
        st.error(f"오류: {data.get('error', '알 수 없음')}")
        return
    
    trades_df = data['trades']
    portfolio_df = data['portfolio']
    ai_logs_df = data['ai_logs']
    
    # 성과 지표 계산
    metrics = calculate_performance_metrics(trades_df)
    
    if not metrics:
        st.warning("⚠️ 거래 데이터가 없습니다.")
        return
    
    # 대시보드 렌더링
    render_performance_overview(metrics)
    
    st.markdown("---")
    
    # 탭으로 구성
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 거래 내역", 
        "📊 포트폴리오 변화", 
        "💰 손익 분석",
        "🧠 AI 분석 상세",
        "📈 AI 결정 분포"
    ])
    
    with tab1:
        render_trades_table(trades_df)
    
    with tab2:
        render_portfolio_chart(portfolio_df)
    
    with tab3:
        render_profit_loss_chart(portfolio_df)
    
    with tab4:
        render_ai_analysis_detailed(ai_logs_df)
    
    with tab5:
        render_ai_decision_chart(ai_logs_df)
    
    # 새로고침 버튼
    st.sidebar.title("🔄 제어판")
    if st.sidebar.button("데이터 새로고침"):
        st.cache_data.clear()
        st.rerun()
    
    # 정보
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 대시보드 정보**")
    st.sidebar.info(f"📅 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not trades_df.empty:
        latest_trade = pd.to_datetime(trades_df['timestamp']).max()
        st.sidebar.info(f"🔄 최근 거래: {latest_trade.strftime('%Y-%m-%d %H:%M')}")
        
        # 추가 통계 정보
        total_trades = len(trades_df)
        successful_trades = len(trades_df[trades_df['success'] == True])
        st.sidebar.info(f"📊 총 거래: {total_trades}건 (성공: {successful_trades}건)")
    
    # AI 분석 통계
    if not ai_logs_df.empty:
        st.sidebar.markdown("**🧠 AI 분석 정보**")
        total_analysis = len(ai_logs_df)
        if 'ai_decision' in ai_logs_df.columns:
            latest_decision = ai_logs_df.iloc[0]['ai_decision'] if len(ai_logs_df) > 0 else 'N/A'
            st.sidebar.info(f"🔍 총 분석: {total_analysis}회")
            st.sidebar.info(f"🎯 최근 결정: {latest_decision}")
        else:
            st.sidebar.info(f"🔍 총 AI 분석: {total_analysis}회")

if __name__ == "__main__":
    main() 