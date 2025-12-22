# AdNexus - Vinmo Investment Tracker 📊

## Overview
An interactive dashboard for tracking the AdNexus-Vinmo investment deal with real-time analytics, projections, and risk analysis.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Usage Guide](#usage-guide)
- [Customization](#customization)
- [Deployment Options](#deployment-options)
- [Sharing with Stakeholders](#sharing-with-stakeholders)
- [Contributing](#contributing)
- [Team Contacts](#team-contacts)
- [Known Issues & Limitations](#known-issues--limitations)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [License](#license)

## Features
- **Real-time Metrics Tracking**: Update current MAU, ARPU, and revenue
- **Dynamic Projections**: See how changes affect repayment timeline
- **Risk Analysis**: Multiple scenarios with probability weighting
- **Unit Economics**: Track LTV/CAC ratios and cohort retention
- **Downloadable Reports**: Export data in CSV, JSON formats

## Prerequisites

Before running the AdNexus Tracker, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager - comes with Python)
- **Git** (for development and version control) - [Download Git](https://git-scm.com/)
- **Docker** (optional, for containerized deployment) - [Download Docker](https://www.docker.com/)

**System Requirements:**
- OS: macOS 10.14+, Windows 10+, or Ubuntu 18.04+
- RAM: 2GB minimum, 4GB recommended
- Disk Space: 500MB minimum

## Quick Start

### Option 1: Streamlit Web App (Recommended) 🚀

#### Installation
```bash
# 1. Install Python (3.8 or higher)
# Download from https://www.python.org/downloads/

# 2. Install required packages
pip install streamlit pandas numpy plotly

# Or install all dependencies
pip install -r requirements.txt
```

#### Running the App
```bash
# Navigate to the app directory
cd /path/to/app

# Run the Streamlit app
streamlit run adnexus_tracker_app.py

# The app will open in your browser at http://localhost:8501
```

#### First Time Setup
1. The app will open with default values (₹10L monthly revenue, 10,000 MAU)
2. Update the sidebar with your current metrics
3. Adjust growth assumptions to match your projections
4. Explore different tabs for detailed analysis

### Option 2: Jupyter Notebook 📓

```bash
# Install Jupyter
pip install jupyter notebook

# Run Jupyter
jupyter notebook adnexus_tracker_notebook.ipynb
```

### Option 3: Docker Container 🐳

```bash
# Build the Docker image
docker build -t adnexus-tracker .

# Run the container
docker run -p 8501:8501 adnexus-tracker
```

## Development Setup

For contributing to this project or working on local development:

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_ORG/adnexus-tracker.git
cd adnexus-tracker
```

### 2. Create Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run adnexus_tracker_app.py
```

### 5. Making Changes
See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development workflow and branching strategy
- Code style guidelines and conventions
- Pull request process
- Testing guidelines

## Usage Guide

### 1. Updating Current Metrics (Sidebar)
- **Current Month #**: Which month you're in (1-60)
- **Current MAU**: Your monthly active users
- **Current ARPU**: Average revenue per user
- **Current Monthly Revenue**: Total monthly revenue in lakhs

### 2. Setting Growth Assumptions
- **Monthly User Growth %**: Expected MAU growth rate
- **Monthly ARPU Growth %**: Expected ARPU improvement
- **Monthly Churn %**: User retention/churn rate

### 3. Understanding the Tabs

#### 📈 Overview Tab
- Key metrics at a glance
- Growth trajectory chart
- Cumulative repayment tracking

#### 💵 Cash Flow Tab
- Detailed monthly projections
- Quarterly summaries
- Download projections as CSV

#### 👥 Unit Economics Tab
- MAU growth tracking
- LTV/CAC ratio evolution
- Cohort retention heatmap

#### ⚠️ Risk Analysis Tab
- Scenario planning (Pessimistic to Best Case)
- Sensitivity analysis matrix
- Key risk factors and mitigation

#### 📊 Reports Tab
- Executive summary generation
- Downloadable reports in multiple formats

## Customization

### Modifying Growth Models
Edit the `calculate_projections()` function in `adnexus_tracker_app.py`:

```python
def calculate_projections(current_revenue, growth_rate, months=48):
    # Modify the growth formula here
    revenue = current_revenue * ((1 + growth_rate/100) ** month)
    # Adjust net revenue calculation
    net_revenue = revenue * 0.25  # Change margin assumptions
```

### Adding New Metrics
Add new input fields in the sidebar:

```python
new_metric = st.sidebar.number_input("New Metric", min_value=0, max_value=100)
```

### Changing Visual Themes
Modify the Plotly themes in any chart:

```python
fig.update_layout(
    template='plotly_dark',  # Change theme
    height=400
)
```

## Deployment Options

### Deploy to Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy with one click

### Deploy to Heroku
```bash
# Create Procfile
echo "web: streamlit run adnexus_tracker_app.py" > Procfile

# Deploy to Heroku
heroku create adnexus-tracker
git push heroku main
```

### Deploy to AWS/GCP/Azure
Use the provided Dockerfile for containerized deployment.

## Sharing with Stakeholders

### For AdNexus Team
1. **Weekly Updates**: Run the app every Monday with latest metrics
2. **Board Meetings**: Generate executive summary from Reports tab
3. **Investor Updates**: Export full projections as CSV

### For Vinmo Team
1. **Monthly Reviews**: Check actual vs projected in Overview tab
2. **Risk Monitoring**: Review Risk Analysis tab for early warnings
3. **Performance Tracking**: Monitor Unit Economics for LTV/CAC trends

## Contributing

We welcome contributions from the team! Here's how you can help:

### Getting Started
1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
2. Check [GitHub Issues](../../issues) for tasks to work on
3. Follow the development setup instructions above

### Quick Contribution Guide
- **Reporting Bugs:** Use the bug report template in GitHub Issues
- **Suggesting Features:** Use the feature request template
- **Submitting Changes:** Create a feature branch and submit a pull request
- **Code Style:** Follow PEP 8 guidelines and add docstrings

### Development Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git commit -m "feat(scope): description"

# Push and create PR
git push origin feature/your-feature-name
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete details on branching strategy, commit conventions, and testing.

## Team Contacts

### Project Leadership
- **Project Owner:** [Name] - [email]@vinmoventures.com
- **Technical Lead:** [Name] - [email]@vinmoventures.com

### Business Contacts
- **Vinmo Ventures:** seema@vinmoventures.com
- **AdNexus Team:** ayush@adnexus.com

### Support
- **Technical Support:** support@vinmoventures.com
- **Security Issues:** security@vinmoventures.com (for vulnerabilities)
- **General Questions:** Use [GitHub Discussions](../../discussions)

## Known Issues & Limitations

### Current Limitations
- **Single-User Only:** Currently supports one user at a time (multi-user support planned for v1.2)
- **No Persistence:** Calculations are session-based; closing the app resets all inputs
- **No Authentication:** No built-in user authentication (see Security Notes for adding auth)
- **No Historical Data:** Cannot store or compare historical projections

### Planned Enhancements
See [CHANGELOG.md](CHANGELOG.md) for detailed roadmap:
- v1.1: Database integration for historical data
- v1.2: Multi-user support with role-based access
- Future: Authentication system, email notifications, API integration

### Workarounds
- **Data Persistence:** Export data regularly using the Reports tab
- **Multi-User:** Use separate browser sessions or deploy multiple instances
- **Authentication:** Add streamlit-authenticator (see Security Notes section)

## Troubleshooting

### Common Issues

**App won't start:**
```bash
# Check Python version (needs 3.8+)
python --version

# Reinstall dependencies
pip install --upgrade streamlit pandas plotly
```

**Charts not showing:**
- Clear browser cache
- Try different browser
- Check firewall settings for port 8501

**Data not updating:**
- Refresh the browser (F5)
- Check if all required fields are filled
- Verify number formats (use decimals, not commas)

## Support & Updates

### Getting Help
- Email: support@vinmoventures.com
- Documentation: Check the inline help (?) icons in the app

### Version History
- v1.0 (Dec 2025): Initial release with core features
- v1.1 (Coming): Add database integration
- v1.2 (Planned): Multi-user support

## Security Notes
- All calculations are done locally
- No data is sent to external servers
- For production use, add authentication:

```python
# Add to app.py for basic auth
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    names=['AdNexus Team', 'Vinmo Team'],
    usernames=['adnexus', 'vinmo'],
    passwords=['hashed_password_1', 'hashed_password_2']
)
```

## License
This tool is provided for AdNexus and Vinmo Ventures internal use only.

---

**Created by:** Vinmo Ventures Investment Team  
**Last Updated:** December 2025  
**Version:** 1.0