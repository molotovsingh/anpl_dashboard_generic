# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AdNexus Investment Tracker is a Streamlit dashboard for monitoring a revenue-share investment deal between Vinmo Ventures and AdNexus. The application calculates investment repayment timelines based on growth projections and provides real-time scenario analysis.

**Investment Structure:**
- Investment: ₹75 Lakhs
- Revenue Share: 5% of net revenue
- Equity: 17.5%
- Target Repayment: 36 months

## Development Commands

### Running the Application

**Quick start (recommended):**
```bash
streamlit run adnexus_tracker_app.py
```

**Using launch scripts:**
```bash
# Mac/Linux
./launch_tracker.sh

# Windows
launch_tracker.bat
```

**Docker:**
```bash
docker build -t adnexus-tracker .
docker run -p 8501:8501 adnexus-tracker
```

**Development setup (with virtual environment):**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or: venv\Scripts\activate  # Windows
pip install -r requirements.txt
streamlit run adnexus_tracker_app.py
```

The app runs on http://localhost:8501

### No Testing Infrastructure

This project currently has no automated tests. When adding features:
- Manually test all sidebar inputs with edge cases (zero values, very large numbers)
- Verify calculations against expected outputs
- Test all download features (CSV, JSON, TXT)
- Check charts render correctly with different data ranges
- Test with different growth rates: low (<3%), moderate (5-7%), high (>10%)

## Architecture & Code Structure

### Single-File Application

The entire application is in `adnexus_tracker_app.py` (~500 lines). No separate modules, classes, or external services.

**High-level flow:**
1. Streamlit page configuration and styling (lines 16-36)
2. Sidebar inputs for current metrics and growth assumptions (lines 43-66)
3. Two core calculation functions (lines 68-116)
4. Five tabs with visualizations (lines 119-490)

### Core Calculation Functions

**`calculate_projections(current_revenue, growth_rate, months=48)`**
- Computes monthly revenue projections until investment is repaid
- Returns DataFrame with: Month, Gross Revenue, Net Revenue, Payment to Vinmo, Cumulative Paid, Balance
- **Key formula:** `revenue = current_revenue * ((1 + growth_rate/100) ** month)`
- **Critical assumptions:**
  - Net margin: 25% of gross revenue
  - Revenue share: 5% of net revenue (NOT gross)
  - Breaks early if cumulative payment >= ₹75L

**`calculate_unit_economics(mau, arpu, growth_rate, months=36)`**
- Tracks MAU, ARPU, LTV, CAC, and LTV/CAC ratio over time
- **Key formulas:**
  - LTV = ARPU × 6 (assumes 6-month average lifetime)
  - CAC = 30 + (month × 2) (increases linearly over time)
  - ARPU grows at fixed 1% monthly regardless of input parameter

### Tab Architecture

Each tab uses Streamlit's tab component and is self-contained:

1. **Overview Tab:** Key metrics + growth trajectory charts
2. **Cash Flow Tab:** Detailed projections table + quarterly summaries + download CSV
3. **Unit Economics Tab:** MAU growth + LTV/CAC trends + cohort retention heatmap
4. **Risk Analysis Tab:** Scenario analysis (4 scenarios) + sensitivity matrix + risk factors table
5. **Reports Tab:** Executive summary + multi-format downloads (CSV, TXT, JSON)

### Data Flow & State Management

**No persistent state:** All calculations are session-based. Closing the app resets everything.

**State management:**
- Sidebar inputs → stored in Streamlit session state automatically
- Each tab re-calculates data when loaded (no caching)
- Downloads create data on-the-fly from current inputs

**Performance note:** No caching implemented. For large datasets or slow calculations, consider adding `@st.cache_data` decorator to calculation functions.

## Important Business Logic & Assumptions

### Financial Calculations

**Revenue to Payment Flow:**
```
Gross Revenue → Net Revenue (25% margin) → Payment to Vinmo (5% of net)
Example: ₹100L gross → ₹25L net → ₹1.25L payment
```

**Repayment Target:**
- Break-even is ₹75L cumulative payment
- Target timeline is 36 months
- If repayment takes >42 months = High Risk

### Growth Model Assumptions

**Three growth scenarios used in charts:**
- Conservative: 5% monthly
- Current: User-defined (default 7.5%)
- Optimistic: 10% monthly

**Churn modeling:**
- Default churn: 20% monthly
- Applied in cohort retention analysis (Tab 3)
- Retention = previous_retention × (1 - churn_rate/100)

**CAC inflation:**
- Starts at ₹30
- Increases by ₹2 per month
- Reflects increasing acquisition difficulty over time

### Sensitivity Analysis (Tab 4)

Tests growth rates: 3%, 5%, 7%, 9%, 11%
Against churn rates: 10%, 15%, 20%, 25%, 30%

Output is months to repayment for each combination.

## Key Constants & Magic Numbers

These values are hardcoded and represent core business assumptions:

```python
investment_amount = 75.0        # ₹75 Lakhs
revenue_share = 5.0             # 5% of net revenue
equity_stake = 17.5             # 17.5% equity
net_margin = 0.25              # 25% net margin assumption
ltv_months = 6                 # 6-month customer lifetime
initial_cac = 30               # Starting CAC in rupees
cac_monthly_increase = 2       # CAC inflation rate
arpu_growth_rate = 0.01        # Fixed 1% monthly in unit economics
target_months = 36             # Target repayment timeline
target_revenue_multiplier = 141 # ₹141L MRR needed for 36-month repayment
ltv_cac_threshold = 3          # Minimum viable LTV/CAC ratio
```

To modify business assumptions, search for these values in the main calculation functions.

## Visualization Stack

**Charts use Plotly:**
- All interactive visualizations use `plotly.graph_objects` or `plotly.express`
- Heatmaps use `go.Heatmap` for sensitivity and cohort analysis
- Time series use `go.Scatter` with `mode='lines+markers'`

**Color scheme:**
- Green: Positive metrics (revenue growth, payments)
- Red: Targets/thresholds (investment amount, minimum ratios)
- RdYlGn: Diverging scale for heatmaps (Red=bad, Green=good)

## Common Modifications

### Changing Investment Terms

Edit sidebar inputs (lines 62-65):
```python
investment_amount = st.sidebar.number_input("Investment Amount (₹ Lakhs)", value=75.0, disabled=True)
```
Remove `disabled=True` to make editable in UI, or change default `value`.

### Adjusting Net Margin Assumption

In `calculate_projections()` function (line 75):
```python
net_revenue = revenue * 0.25  # Change 0.25 to new margin
```

### Modifying LTV Calculation

In `calculate_unit_economics()` function (line 100):
```python
ltv = current_arpu * 6  # Change 6 to new lifetime in months
```

### Adding New Metrics to Overview

Insert new column in line 123:
```python
col1, col2, col3, col4, col5, col6 = st.columns(6)  # Add col7 for new metric
```

Then add metric display:
```python
col7.metric("New Metric", f"Value", "Delta")
```

## Deployment Context

This is a **private internal tool** for Vinmo Ventures and AdNexus teams only:
- Contains business-sensitive financial projections
- No authentication built-in (add before deploying to production)
- Proprietary license - not open source
- Data is ephemeral (no database)

Deploy via:
- Streamlit Cloud (easiest)
- Docker (provided Dockerfile)
- Heroku/AWS/GCP (containerized)

See DEPLOYMENT_GUIDE.md for detailed instructions.
