# 📦 AdNexus Investment Tracker - Deployment Package

## What's Included

This package contains everything needed to run the AdNexus-Vinmo investment tracking dashboard:

```
adnexus-tracker/
│
├── 📊 adnexus_tracker_app.py      # Main Streamlit application
├── 📄 requirements.txt            # Python dependencies
├── 📖 README.md                   # Documentation
├── 🚀 launch_tracker.sh           # Mac/Linux launcher
├── 🚀 launch_tracker.bat          # Windows launcher  
├── 🐳 Dockerfile                  # Docker container setup
├── 📈 AdNexus_Robust_Analysis.xlsx # Sample data/templates
└── 📝 Investment_Memo.md          # Investment analysis memo
```

## 🚀 Quick Start (3 Ways to Run)

### Method 1: One-Click Launch (Easiest)

**Windows Users:**
1. Double-click `launch_tracker.bat`
2. App opens automatically in browser

**Mac/Linux Users:**
1. Open terminal in this folder
2. Run: `chmod +x launch_tracker.sh` (first time only)
3. Run: `./launch_tracker.sh`
4. App opens automatically in browser

### Method 2: Manual Setup

```bash
# Install dependencies
pip install streamlit pandas numpy plotly

# Run the app
streamlit run adnexus_tracker_app.py
```

### Method 3: Docker (Most Reliable)

```bash
# Build container
docker build -t adnexus-tracker .

# Run container
docker run -p 8501:8501 adnexus-tracker

# Open browser to http://localhost:8501
```

## 📱 How to Use the Dashboard

### Daily Usage (For AdNexus Team)

1. **Morning Check (5 mins)**
   - Open the tracker
   - Update sidebar with yesterday's metrics
   - Check if you're on track (Overview tab)
   - Note any alerts in Risk Analysis

2. **Weekly Review (15 mins)**
   - Update all metrics thoroughly
   - Generate weekly report (Reports tab)
   - Share summary with team
   - Adjust growth assumptions if needed

3. **Monthly Deep Dive (30 mins)**
   - Full metrics update
   - Review all tabs thoroughly
   - Export full cash flow projections
   - Send update to Vinmo

### For Investor Updates (Vinmo)

1. **Quick Status Check**
   - Overview tab shows all key metrics
   - Green = on track, Yellow = attention needed, Red = action required

2. **Detailed Analysis**
   - Cash Flow tab for payment projections
   - Unit Economics for business health
   - Risk Analysis for scenario planning

3. **Report Generation**
   - Reports tab → Download Executive Summary
   - Share in board meetings or investor calls

## 🎯 Key Features Explained

### Real-Time Projections
- Change any input → instantly see impact on repayment timeline
- Try different growth scenarios
- Understand sensitivity to key variables

### Risk Dashboard
- **Probability-weighted outcomes** - Not just best/worst case
- **Sensitivity matrix** - How growth vs churn affects timeline
- **Early warning system** - Know when you're off track

### Unit Economics Tracking
- **LTV/CAC trends** - Is your unit economics improving?
- **Cohort analysis** - Are users sticking around?
- **Growth efficiency** - Is marketing spend working?

## 🔧 Customization Guide

### Adding Your Logo/Branding

Edit `adnexus_tracker_app.py`:

```python
# Add after imports
st.set_page_config(
    page_title="Your Company Tracker",
    page_icon="your_logo.png",
    layout="wide"
)

# Add logo to sidebar
st.sidebar.image("your_logo.png", width=200)
```

### Changing Financial Assumptions

Find these lines to modify:

```python
# Net margin assumption (line ~100)
net_revenue = revenue * 0.25  # Change 0.25 to your margin

# Revenue share percentage (line ~101)
payment = net_revenue * 0.05  # Change 0.05 to your share

# Investment amount (line ~60)
investment_amount = st.sidebar.number_input("Investment Amount", value=75.0)
```

### Adding New Metrics

```python
# Add to sidebar (line ~40)
new_metric = st.sidebar.number_input(
    "Customer Satisfaction Score",
    min_value=0.0,
    max_value=10.0,
    value=8.0
)

# Use in calculations
adjusted_growth = monthly_user_growth * (new_metric / 10)
```

## 🚢 Deployment Options

### Option 1: Local Computer (Development)
- Best for: Testing, development
- Cost: Free
- Setup: 5 minutes

### Option 2: Streamlit Cloud (Recommended)
- Best for: Sharing with team
- Cost: Free
- Setup: 10 minutes
- URL: your-app.streamlit.app

Steps:
1. Upload code to GitHub
2. Go to share.streamlit.io
3. Connect repo
4. Deploy

### Option 3: Company Server
- Best for: Security, control
- Cost: Varies
- Setup: 30 minutes

Using Docker:
```bash
docker-compose up -d
```

### Option 4: Cloud Platforms

**Heroku:**
```bash
heroku create adnexus-tracker
git push heroku main
```

**AWS EC2:**
```bash
# Use provided Dockerfile
aws ecs create-service --service-name adnexus-tracker
```

## 📊 Data Management

### Importing Historical Data

Create CSV file with columns:
```
Month,MAU,ARPU,Revenue,Payment_to_Vinmo
1,10000,100,10.0,0.125
2,10750,102,10.97,0.137
```

Load in app:
```python
historical_data = pd.read_csv('historical.csv')
```

### Exporting Reports

All reports can be exported as:
- **CSV** - For Excel analysis
- **JSON** - For API integration
- **PDF** - For presentations (coming soon)

## ⚠️ Troubleshooting

### Issue: "Command not found: streamlit"
**Solution:**
```bash
pip install streamlit
# or
python -m pip install streamlit
```

### Issue: "Port 8501 already in use"
**Solution:**
```bash
# Kill existing process
kill $(lsof -t -i:8501)
# Or use different port
streamlit run app.py --server.port 8502
```

### Issue: Charts not displaying
**Solution:**
- Clear browser cache
- Update plotly: `pip install --upgrade plotly`
- Try different browser

### Issue: Can't install packages
**Solution:**
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## 🔒 Security Best Practices

### For Production Use

1. **Add Authentication:**
```python
# Add to top of app.py
import streamlit_authenticator as stauth

names = ['AdNexus Team', 'Vinmo Team']
usernames = ['adnexus', 'vinmo']
passwords = ['$2b$12$xxx', '$2b$12$yyy']  # Hashed

authenticator = stauth.Authenticate(
    names, usernames, passwords,
    'cookie_name', 'signature_key', 30
)

name, auth_status, username = authenticator.login('Login', 'main')

if not auth_status:
    st.stop()
```

2. **Secure Deployment:**
- Use HTTPS only
- Set environment variables for sensitive data
- Regular security updates

3. **Data Protection:**
- Don't commit real data to Git
- Use `.env` files for configuration
- Encrypt sensitive metrics

## 📞 Support Contacts

### Technical Issues
- Email: tech-support@vinmoventures.com
- Slack: #adnexus-tracker-help

### Business Questions
- Investment Team: seema@vinmoventures.com
- AdNexus Lead: ayush@adnexus.com

### Feature Requests
Submit via GitHub Issues or email

## 📅 Update Schedule

- **Weekly:** Metric updates (AdNexus team)
- **Monthly:** Full review and projections
- **Quarterly:** Model recalibration if needed

## ✅ Pre-Launch Checklist

Before going live:

- [ ] Update all current metrics in sidebar
- [ ] Verify growth assumptions are realistic
- [ ] Test all download buttons work
- [ ] Check calculations match your Excel
- [ ] Set up regular update reminders
- [ ] Share access with relevant stakeholders
- [ ] Backup initial configuration

---

**Version:** 1.0  
**Last Updated:** December 2025  
**Next Review:** January 2026

Remember: This tool is only as good as the data you input. Keep metrics updated for accurate projections!