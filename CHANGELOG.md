# Changelog

All notable changes to the AdNexus Investment Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Database integration for historical data persistence
- Multi-user support with role-based access
- Authentication and authorization system
- Email notifications for milestone achievements
- API for external integrations

## [1.0.0] - 2025-12-22

### Added
- Initial release of AdNexus Investment Tracker
- Real-time metrics tracking (MAU, ARPU, Revenue)
- Dynamic revenue projections with multiple scenarios
- Risk analysis with probability-weighted outcomes
- Unit economics tracking (LTV/CAC ratios)
- Cohort retention analysis
- Downloadable reports (CSV, JSON formats)
- Interactive dashboard with 5 main tabs:
  - Overview with key metrics
  - Cash Flow projections
  - Unit Economics analysis
  - Risk Analysis scenarios
  - Reports generation
- Docker support for containerized deployment
- Cross-platform launch scripts (bash/bat)
- Comprehensive documentation (README, DEPLOYMENT_GUIDE)

### Features
- **Projection Engine**: Calculate repayment timeline based on growth assumptions
- **Scenario Analysis**: Pessimistic, Base, Optimistic, and Best Case scenarios
- **Sensitivity Matrix**: Visual heatmap for growth vs churn analysis
- **Quarterly Summaries**: Aggregated financial reporting
- **Executive Reports**: Auto-generated investment summaries

### Documentation
- README.md with quick start guide
- DEPLOYMENT_GUIDE.md with multiple deployment options
- Inline help and tooltips throughout the app
- Code comments and docstrings

### Technical Stack
- Python 3.9+
- Streamlit 1.29.0+
- Pandas, NumPy for data processing
- Plotly for interactive visualizations
- Docker for containerization

---

## Version History

**Legend:**
- `Added` - New features
- `Changed` - Changes to existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security improvements

---

**Contributors:** Vinmo Ventures Investment Team
**Last Updated:** December 22, 2025
