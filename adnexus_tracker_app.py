"""
AdNexus - Vinmo Investment Tracker
Interactive Dashboard for Revenue Share Analysis
Created: December 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import plotly.figure_factory as ff

# Page configuration
st.set_page_config(
    page_title="AdNexus Investment Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🚀 AdNexus - Vinmo Ventures Investment Tracker")
st.markdown("### Real-time Revenue Share & Growth Analytics Dashboard")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("📊 Current Metrics")
st.sidebar.markdown("Update your actuals here:")

# Current metrics inputs
current_month = st.sidebar.number_input("Current Month #", min_value=1, max_value=60, value=1)
current_mau = st.sidebar.number_input("Current MAU", min_value=1000, max_value=1000000, value=10000, step=1000)
current_arpu = st.sidebar.number_input("Current ARPU (₹)", min_value=10, max_value=1000, value=100, step=10)
current_monthly_revenue = st.sidebar.number_input("Current Monthly Revenue (₹ Lakhs)", min_value=1.0, max_value=1000.0, value=10.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.header("🎯 Growth Assumptions")

# Growth inputs
monthly_user_growth = st.sidebar.slider("Monthly User Growth %", min_value=0.0, max_value=20.0, value=7.5, step=0.5)
monthly_arpu_growth = st.sidebar.slider("Monthly ARPU Growth %", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
churn_rate = st.sidebar.slider("Monthly Churn %", min_value=5.0, max_value=30.0, value=20.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.header("💰 Investment Terms")
investment_amount = st.sidebar.number_input("Investment Amount (₹ Lakhs)", value=75.0, disabled=True)
revenue_share = st.sidebar.number_input("Revenue Share %", value=5.0, disabled=True)
equity_stake = st.sidebar.number_input("Equity Stake %", value=17.5, disabled=True)

# Main calculation functions
def calculate_projections(current_revenue, growth_rate, redemption_rate=50, revenue_share_pct=5, months=48):
    """
    Calculate monthly revenue projections until investment is repaid.

    Args:
        current_revenue: Starting monthly revenue (₹ Lakhs)
        growth_rate: Monthly growth rate (%)
        redemption_rate: Percentage of revenue that is redeemed (%, default: 50)
        revenue_share_pct: Percentage of net revenue paid to investor (%, default: 5)
        months: Maximum months to project (default: 48)

    Returns:
        DataFrame with monthly projections
    """
    projections = []
    cumulative_payment = 0

    for month in range(months):
        # Month 1 should have 1 month of growth, not 0
        month_number = month + 1

        # Calculate gross revenue with compound growth
        gross_revenue = current_revenue * ((1 + growth_rate/100) ** month_number)

        # Calculate net revenue after redemptions
        redemption_amount = gross_revenue * (redemption_rate / 100)
        net_revenue = gross_revenue - redemption_amount

        # Calculate payment to investor
        payment = net_revenue * (revenue_share_pct / 100)
        cumulative_payment += payment

        projections.append({
            'Month': month_number,
            'Gross Revenue (₹L)': round(gross_revenue, 2),
            'Redemptions (₹L)': round(redemption_amount, 2),
            'Net Revenue (₹L)': round(net_revenue, 2),
            'Payment to Vinmo (₹L)': round(payment, 2),
            'Cumulative Paid (₹L)': round(cumulative_payment, 2),
            'Balance (₹L)': max(0, 75 - cumulative_payment)
        })

        if cumulative_payment >= 75:
            break

    return pd.DataFrame(projections)

def calculate_unit_economics(mau, arpu, user_growth_rate, arpu_growth_rate, churn_rate,
                             ltv_method='churn_based', ltv_months=6,
                             starting_cac=30, cac_monthly_increase=2, months=36):
    """
    Calculate unit economics over time.

    Args:
        mau: Starting Monthly Active Users
        arpu: Starting Average Revenue Per User (₹)
        user_growth_rate: Monthly user growth (%)
        arpu_growth_rate: Monthly ARPU growth (%)
        churn_rate: Monthly churn rate (%)
        ltv_method: 'churn_based' or 'fixed_months'
        ltv_months: Months for LTV if using fixed method
        starting_cac: Initial Customer Acquisition Cost (₹)
        cac_monthly_increase: CAC increase per month (₹)
        months: Months to project

    Returns:
        DataFrame with unit economics metrics
    """
    data = []

    for month in range(months):
        month_number = month + 1

        # Apply compound growth (consistent with projections)
        projected_mau = mau * ((1 + user_growth_rate/100) ** month_number)
        projected_arpu = arpu * ((1 + arpu_growth_rate/100) ** month_number)

        # Calculate LTV based on selected method
        if ltv_method == 'churn_based':
            # LTV = ARPU / churn_rate (geometric series)
            ltv = projected_arpu / (churn_rate / 100) if churn_rate > 0 else projected_arpu * ltv_months
        else:
            # Fixed months method
            ltv = projected_arpu * ltv_months

        # Calculate CAC with linear increase
        cac = starting_cac + (month * cac_monthly_increase)

        # Calculate LTV/CAC ratio
        ltv_cac = ltv / cac if cac > 0 else 0

        data.append({
            'Month': month_number,
            'MAU': int(projected_mau),
            'ARPU': round(projected_arpu, 2),
            'LTV': round(ltv, 2),
            'CAC': round(cac, 2),
            'LTV/CAC': round(ltv_cac, 2)
        })

    return pd.DataFrame(data)

# Default assumption parameters (can be overridden in Assumptions tab)
redemption_rate = 50.0  # Percentage of gross revenue that is redeemed
ltv_method = 'churn_based'  # LTV calculation method: 'churn_based' or 'fixed_months'
ltv_months = 6  # Months for LTV if using fixed method
starting_cac = 30  # Initial Customer Acquisition Cost (₹)
cac_monthly_increase = 2.0  # CAC increase per month (₹)

# Calculate combined revenue growth rate (Revenue = MAU × ARPU)
# Revenue growth = (1 + MAU_growth) × (1 + ARPU_growth) - 1
revenue_growth_rate = ((1 + monthly_user_growth/100) * (1 + monthly_arpu_growth/100) - 1) * 100

# Create main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Overview", "💵 Cash Flow", "👥 Unit Economics", "⚠️ Risk Analysis", "📊 Reports", "🔧 Assumptions"])

# Tab 1: Overview
with tab1:
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    # Calculate key metrics
    df_projections = calculate_projections(current_monthly_revenue, revenue_growth_rate,
                                          redemption_rate=redemption_rate,
                                          revenue_share_pct=revenue_share)
    months_to_repay = len(df_projections)
    final_revenue = df_projections.iloc[-1]['Gross Revenue (₹L)'] if len(df_projections) > 0 else 0
    growth_multiple = final_revenue / current_monthly_revenue if current_monthly_revenue > 0 else 0
    
    # Display metrics
    col1.metric("Current MRR", f"₹{current_monthly_revenue}L", f"+{revenue_growth_rate:.1f}% growth")
    col2.metric("Months to Repay", f"{months_to_repay}", f"Target: 36")
    col3.metric("Required Multiple", f"{growth_multiple:.1f}x", "From current")
    col4.metric("Current MAU", f"{current_mau:,}", f"+{int(current_mau * monthly_user_growth/100)} monthly")
    col5.metric("Current ARPU", f"₹{current_arpu}", f"+{monthly_arpu_growth}%")

    # Calculate current monthly payment with correct formula
    current_net_revenue = current_monthly_revenue * (1 - redemption_rate/100)
    current_payment = current_net_revenue * (revenue_share/100)
    col6.metric("Monthly Payment", f"₹{current_payment:.2f}L", "To Vinmo")
    
    st.markdown("---")
    
    # Growth trajectory chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Revenue Growth Trajectory")
        
        # Create multiple scenarios (revenue growth rates)
        scenarios = {
            'Conservative (5%)': 5.0,
            f'Current ({revenue_growth_rate:.1f}%)': revenue_growth_rate,
            'Optimistic (12%)': 12.0
        }

        fig = go.Figure()
        for name, rate in scenarios.items():
            df_scenario = calculate_projections(current_monthly_revenue, rate,
                                               redemption_rate=redemption_rate,
                                               revenue_share_pct=revenue_share, months=48)
            fig.add_trace(go.Scatter(
                x=df_scenario['Month'],
                y=df_scenario['Gross Revenue (₹L)'],
                name=name,
                mode='lines',
                line=dict(width=2 if abs(rate - revenue_growth_rate) < 0.01 else 1)
            ))
        
        fig.add_hline(y=141, line_dash="dash", line_color="red", 
                     annotation_text="Target for 3-year repayment: ₹141L")
        
        fig.update_layout(
            height=400,
            xaxis_title="Months",
            yaxis_title="Monthly Revenue (₹ Lakhs)",
            hovermode='x unified',
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Cumulative Repayment")
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_projections['Month'],
            y=df_projections['Cumulative Paid (₹L)'],
            name='Paid to Vinmo',
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='green', width=2)
        ))
        
        fig2.add_hline(y=75, line_dash="dash", line_color="red",
                      annotation_text="Investment Amount: ₹75L")
        
        fig2.update_layout(
            height=400,
            xaxis_title="Months",
            yaxis_title="Cumulative Payment (₹ Lakhs)",
            hovermode='x unified'
        )
        st.plotly_chart(fig2, use_container_width=True)

# Tab 2: Cash Flow Analysis
with tab2:
    st.subheader("💵 Detailed Cash Flow Projections")
    
    # Cash flow table
    df_cashflow = calculate_projections(current_monthly_revenue, revenue_growth_rate,
                                       redemption_rate=redemption_rate,
                                       revenue_share_pct=revenue_share, months=48)
    
    # Add quarterly summary
    df_cashflow['Quarter'] = (df_cashflow['Month'] - 1) // 3 + 1
    df_quarterly = df_cashflow.groupby('Quarter').agg({
        'Gross Revenue (₹L)': 'sum',
        'Payment to Vinmo (₹L)': 'sum',
        'Cumulative Paid (₹L)': 'last',
        'Balance (₹L)': 'last'
    }).round(2)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Monthly Projections")
        st.dataframe(df_cashflow, height=400, use_container_width=True)
        
        # Download button
        csv = df_cashflow.to_csv(index=False)
        st.download_button(
            label="📥 Download Monthly Projections",
            data=csv,
            file_name=f"adnexus_projections_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv'
        )
    
    with col2:
        st.markdown("### Quarterly Summary")
        st.dataframe(df_quarterly, use_container_width=True)
        
        # Key insights
        st.markdown("### 💡 Key Insights")
        if months_to_repay <= 36:
            st.success(f"✅ On track to repay within target (36 months)")
        else:
            st.warning(f"⚠️ Repayment will take {months_to_repay - 36} months longer than target")
        
        break_even_month = df_cashflow[df_cashflow['Cumulative Paid (₹L)'] >= 37.5].iloc[0]['Month'] if len(df_cashflow[df_cashflow['Cumulative Paid (₹L)'] >= 37.5]) > 0 else None
        if break_even_month:
            st.info(f"📊 50% repayment milestone: Month {break_even_month}")

# Tab 3: Unit Economics
with tab3:
    st.subheader("👥 Unit Economics & User Metrics")
    
    df_unit = calculate_unit_economics(current_mau, current_arpu, monthly_user_growth,
                                       monthly_arpu_growth, churn_rate,
                                       ltv_method=ltv_method, ltv_months=ltv_months,
                                       starting_cac=starting_cac,
                                       cac_monthly_increase=cac_monthly_increase)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### MAU Growth")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=df_unit['Month'],
            y=df_unit['MAU'],
            mode='lines+markers',
            name='Monthly Active Users',
            fill='tozeroy',
            line=dict(color='blue', width=2)
        ))
        fig3.update_layout(
            height=350,
            xaxis_title="Months",
            yaxis_title="MAU",
            hovermode='x unified'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("### LTV/CAC Ratio")
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=df_unit['Month'],
            y=df_unit['LTV/CAC'],
            mode='lines+markers',
            name='LTV/CAC',
            line=dict(color='green', width=2)
        ))
        fig4.add_hline(y=3, line_dash="dash", line_color="red",
                      annotation_text="Minimum Viable: 3x")
        fig4.update_layout(
            height=350,
            xaxis_title="Months",
            yaxis_title="LTV/CAC Ratio",
            hovermode='x unified'
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Cohort Analysis
    st.markdown("### 📊 Cohort Retention Analysis")
    
    # Create sample cohort data
    cohort_data = []
    for cohort_month in range(1, 7):
        retention = [100]
        for month in range(1, 13):
            retention.append(retention[-1] * (1 - churn_rate/100))
        cohort_data.append(retention[:13])
    
    cohort_df = pd.DataFrame(cohort_data, 
                             columns=[f'M{i}' for i in range(13)],
                             index=[f'Cohort {i}' for i in range(1, 7)])
    
    fig5 = go.Figure(data=go.Heatmap(
        z=cohort_df.values,
        x=cohort_df.columns,
        y=cohort_df.index,
        colorscale='RdYlGn',
        text=cohort_df.values.round(1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        hovertemplate='Cohort: %{y}<br>Month: %{x}<br>Retention: %{z:.1f}%<extra></extra>'
    ))
    
    fig5.update_layout(
        height=300,
        xaxis_title="Months Since Acquisition",
        yaxis_title="Cohort",
        title="User Retention by Cohort (%)"
    )
    st.plotly_chart(fig5, use_container_width=True)

# Tab 4: Risk Analysis
with tab4:
    st.subheader("⚠️ Risk Scenarios & Sensitivity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Scenario Analysis")
        
        scenarios_data = {
            'Scenario': ['Pessimistic', 'Base Case', 'Optimistic', 'Best Case'],
            'Growth Rate': [5.0, revenue_growth_rate, 10.0, 12.0],
            'Probability': [20, 50, 25, 5],
            'Months to Repay': []
        }
        
        # Calculate months for each scenario
        for rate in scenarios_data['Growth Rate']:
            df_temp = calculate_projections(current_monthly_revenue, rate,
                                           redemption_rate=redemption_rate,
                                           revenue_share_pct=revenue_share)
            months = len(df_temp)
            scenarios_data['Months to Repay'].append(months)
        
        df_scenarios = pd.DataFrame(scenarios_data)
        st.dataframe(df_scenarios, use_container_width=True)
        
        # Expected outcome
        expected_months = sum(df_scenarios['Probability'] * df_scenarios['Months to Repay']) / 100
        st.metric("Expected Repayment", f"{expected_months:.1f} months", 
                 f"{expected_months - 36:.1f} vs target" if expected_months > 36 else "On target")
    
    with col2:
        st.markdown("### Sensitivity Analysis")
        
        # Create sensitivity matrix
        growth_rates = [3, 5, 7, 9, 11]
        churn_rates = [10, 15, 20, 25, 30]
        
        sensitivity_matrix = []
        for churn in churn_rates:
            row = []
            for growth in growth_rates:
                df_temp = calculate_projections(current_monthly_revenue, growth,
                                               redemption_rate=redemption_rate,
                                               revenue_share_pct=revenue_share)
                months = len(df_temp)
                row.append(months if months <= 60 else '>60')
            sensitivity_matrix.append(row)
        
        fig6 = go.Figure(data=go.Heatmap(
            z=[[float(x) if x != '>60' else 60 for x in row] for row in sensitivity_matrix],
            x=[f'{g}%' for g in growth_rates],
            y=[f'{c}%' for c in churn_rates],
            colorscale='RdYlGn_r',
            text=sensitivity_matrix,
            texttemplate='%{text}',
            textfont={"size": 12}
        ))
        
        fig6.update_layout(
            height=350,
            xaxis_title="Monthly Growth Rate",
            yaxis_title="Churn Rate",
            title="Months to Repayment (Sensitivity)"
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    # Risk factors
    st.markdown("### 🎯 Key Risk Factors")
    
    risk_data = {
        'Risk Factor': [
            'CAC Inflation',
            'Higher Churn',
            'Competition',
            'Regulatory',
            'Platform Issues'
        ],
        'Probability': ['High', 'Medium', 'High', 'Low', 'Low'],
        'Impact': ['+6 months', '+4 months', '+8 months', '+12 months', '+3 months'],
        'Mitigation': [
            'Diversify channels',
            'Improve retention',
            'Unique value prop',
            'Compliance framework',
            'Tech redundancy'
        ]
    }
    
    df_risks = pd.DataFrame(risk_data)
    st.dataframe(df_risks, use_container_width=True)

# Tab 5: Reports
with tab5:
    st.subheader("📊 Executive Reports")
    
    # Generate executive summary
    st.markdown("### Executive Summary")

    # Calculate current payment with correct formula
    exec_current_net_revenue = current_monthly_revenue * (1 - redemption_rate/100)
    exec_current_payment = exec_current_net_revenue * (revenue_share/100)

    summary = f"""
    **Investment Analysis as of {datetime.now().strftime('%B %d, %Y')}**

    **Current Performance:**
    - Monthly Revenue: ₹{current_monthly_revenue} Lakhs
    - Monthly Active Users: {current_mau:,}
    - Average Revenue per User: ₹{current_arpu}
    - Monthly Payment to Vinmo: ₹{exec_current_payment:.2f} Lakhs
    
    **Projections (at {revenue_growth_rate:.1f}% monthly revenue growth):**
    - Expected Repayment: {months_to_repay} months
    - Required Growth Multiple: {growth_multiple:.1f}x
    - Final Monthly Revenue: ₹{final_revenue:.1f} Lakhs
    
    **Investment Structure:**
    - Total Investment: ₹{investment_amount} Lakhs
    - Revenue Share: {revenue_share}%
    - Equity Stake: {equity_stake}%
    
    **Risk Assessment:**
    - {'✅ Low Risk' if months_to_repay <= 30 else '⚠️ Moderate Risk' if months_to_repay <= 42 else '🔴 High Risk'}
    - {'On track for target timeline' if months_to_repay <= 36 else f'Behind target by {months_to_repay - 36} months'}
    
    **Recommendation:**
    {'Continue current growth strategy' if monthly_user_growth >= 7.5 else 'Consider increasing marketing spend and user acquisition efforts'}
    """
    
    st.markdown(summary)
    
    # Generate downloadable report
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📥 Download Full Report (CSV)",
            data=df_projections.to_csv(index=False),
            file_name=f"adnexus_full_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv'
        )
    
    with col2:
        st.download_button(
            label="📥 Download Executive Summary",
            data=summary,
            file_name=f"adnexus_executive_summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime='text/plain'
        )
    
    with col3:
        # Create combined data for download
        combined_data = {
            'Projections': df_projections.to_dict(),
            'Unit Economics': df_unit.to_dict(),
            'Scenarios': df_scenarios.to_dict()
        }
        
        import json
        st.download_button(
            label="📥 Download All Data (JSON)",
            data=json.dumps(combined_data, indent=2),
            file_name=f"adnexus_all_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime='application/json'
        )

# Tab 6: Assumptions
with tab6:
    st.subheader("🔧 Business Assumptions & Parameters")

    st.markdown("### 📊 Financial Model Parameters")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Revenue Model")
        redemption_rate_input = st.slider(
            "Redemption Rate (%)",
            min_value=0.0,
            max_value=80.0,
            value=redemption_rate,
            step=1.0,
            help="Percentage of gross revenue that is redeemed/returned",
            key="redemption_rate_input"
        )

        revenue_share_input = st.slider(
            "Revenue Share to Investor (%)",
            min_value=0.0,
            max_value=20.0,
            value=revenue_share,
            step=0.5,
            help="Percentage of net revenue paid to Vinmo Ventures",
            key="revenue_share_input"
        )

        # Show calculated effective rate
        effective_rate = (100 - redemption_rate_input) / 100 * revenue_share_input
        st.info(f"**Effective Payment Rate:** {effective_rate:.2f}% of gross revenue")

    with col2:
        st.markdown("#### Unit Economics")

        ltv_method_input = st.radio(
            "LTV Calculation Method",
            options=['churn_based', 'fixed_months'],
            format_func=lambda x: 'Churn-Based (Recommended)' if x == 'churn_based' else 'Fixed Months',
            help="Churn-based uses: LTV = ARPU / churn_rate",
            key="ltv_method_input",
            index=0 if ltv_method == 'churn_based' else 1
        )

        if ltv_method_input == 'fixed_months':
            ltv_months_input = st.slider("LTV Months", 1, 24, ltv_months, key="ltv_months_input")
        else:
            ltv_months_input = ltv_months  # Use default

        starting_cac_input = st.number_input(
            "Starting CAC (₹)",
            min_value=0,
            max_value=500,
            value=starting_cac,
            step=5,
            help="Initial Customer Acquisition Cost",
            key="starting_cac_input"
        )

        cac_increase_input = st.slider(
            "CAC Monthly Increase (₹)",
            min_value=0.0,
            max_value=10.0,
            value=cac_monthly_increase,
            step=0.5,
            help="How much CAC increases each month",
            key="cac_increase_input"
        )

    st.markdown("---")
    st.markdown("### 📋 Current Assumptions Summary")

    # Display all assumptions in organized format
    assumptions_summary = f"""**Revenue Model:**
- Gross Revenue Growth: {revenue_growth_rate:.2f}% monthly (MAU × ARPU growth)
- Redemption Rate: {redemption_rate_input}%
- Net Revenue: Gross × {100-redemption_rate_input}%
- Payment to Investor: Net Revenue × {revenue_share_input}%
- Effective Rate: {effective_rate:.2f}% of gross revenue

**Growth Assumptions:**
- User Growth: {monthly_user_growth}% monthly
- ARPU Growth: {monthly_arpu_growth}% monthly
- Churn Rate: {churn_rate}% monthly

**Unit Economics:**
- LTV Method: {"Churn-Based" if ltv_method_input == 'churn_based' else f"Fixed ({ltv_months_input} months)"}
- Starting CAC: ₹{starting_cac_input}
- CAC Increase: ₹{cac_increase_input}/month

**Investment Terms:**
- Investment Amount: ₹{investment_amount} Lakhs
- Revenue Share: {revenue_share_input}%
- Equity Stake: {equity_stake}%
"""

    st.text(assumptions_summary)

    # Download assumptions
    st.download_button(
        label="📥 Download Assumptions",
        data=assumptions_summary,
        file_name=f"adnexus_assumptions_{datetime.now().strftime('%Y%m%d')}.txt",
        mime='text/plain'
    )

    st.markdown("---")
    st.markdown("### 💡 Assumptions Guide")

    with st.expander("Understanding Redemption Rate"):
        st.markdown("""
**Redemption Rate** is the percentage of gross revenue that customers redeem/return.

- Higher redemption = Lower net revenue = Longer repayment
- Current: ~50% (meaning 50% of gross is redeemed)
- Net Revenue = Gross × (100% - 50%) = Gross × 50%

**Example:**
- Gross Revenue: ₹10L
- Redemption Rate: 50%
- Redemptions: ₹10L × 50% = ₹5L
- Net Revenue: ₹10L - ₹5L = ₹5L
- Payment (5% of net): ₹5L × 5% = ₹0.25L
        """)

    with st.expander("Understanding LTV Calculation Methods"):
        st.markdown("""
**Churn-Based (Recommended):**
- LTV = ARPU ÷ Churn Rate
- Example: ₹100 ARPU, 20% churn → LTV = ₹100 / 0.20 = ₹500
- Automatically adjusts when churn changes
- More accurate representation of customer lifetime value

**Fixed Months:**
- LTV = ARPU × Number of Months
- Example: ₹100 ARPU, 6 months → LTV = ₹600
- Simple but doesn't account for churn
- Useful for quick estimates

**Note:** The churn-based method is more realistic for subscription businesses.
        """)

    with st.expander("Understanding CAC (Customer Acquisition Cost)"):
        st.markdown("""
**CAC** is the cost to acquire one new customer.

- Lower CAC = More efficient marketing
- CAC typically increases over time as easy channels saturate
- Target: LTV/CAC ratio > 3 for healthy unit economics

**Current Settings:**
- Starting CAC: ₹{0}
- Monthly Increase: ₹{1}/month
- This means in Month 1 CAC = ₹{0}, Month 2 = ₹{2}, etc.

**Why does CAC increase?**
- Early adopters are easier to acquire
- Marketing channels become saturated
- Competition increases over time
        """.format(starting_cac_input, cac_increase_input, starting_cac_input + cac_increase_input))

    with st.expander("Understanding Revenue Share Model"):
        st.markdown("""
**How the Deal Works:**
1. AdNexus generates gross revenue each month
2. Customers redeem a portion (currently ~50%)
3. Net Revenue = Gross Revenue - Redemptions
4. Vinmo receives 5% of Net Revenue until ₹75L is repaid

**Key Point:** This is a revenue share deal, NOT a profit share deal. Payments are made regardless of profitability.

**Example Month:**
- Gross Revenue: ₹10L
- Redemptions (50%): ₹5L
- Net Revenue: ₹5L
- Payment to Vinmo (5%): ₹0.25L
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p>AdNexus - Vinmo Ventures Investment Tracker v1.0</p>
        <p>For internal use only | Data updated in real-time</p>
    </div>
    """, unsafe_allow_html=True)