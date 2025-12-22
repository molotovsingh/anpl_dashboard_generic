# Contributing to AdNexus Investment Tracker

Thank you for your interest in contributing to the AdNexus Investment Tracker! We're excited to have you here. This document will guide you through the contribution process.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Code Style Guidelines](#code-style-guidelines)
- [Making Changes](#making-changes)
- [Commit Message Conventions](#commit-message-conventions)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Getting Help](#getting-help)

## Getting Started

Before you begin:
1. Read the [README.md](README.md) to understand the project
2. Check the [GitHub Issues](../../issues) for existing work
3. Review this guide completely

## Development Environment Setup

### Prerequisites
- Python 3.8 or higher
- Git installed and configured
- Basic knowledge of Streamlit and Pandas

### Setup Steps

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/adnexus-tracker.git
   cd adnexus-tracker
   ```

2. **Create Virtual Environment**
   ```bash
   # Create environment
   python -m venv venv

   # Activate (Mac/Linux)
   source venv/bin/activate

   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   streamlit run adnexus_tracker_app.py
   ```
   The app should open at http://localhost:8501

## Project Structure

```
adnexus-tracker/
├── adnexus_tracker_app.py    # Main Streamlit application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── launch_tracker.sh          # Mac/Linux launcher
├── launch_tracker.bat         # Windows launcher
├── README.md                  # User documentation
├── DEPLOYMENT_GUIDE.md        # Deployment instructions
├── CONTRIBUTING.md            # This file
├── CHANGELOG.md               # Version history
└── .github/                   # GitHub templates
    ├── ISSUE_TEMPLATE/
    └── pull_request_template.md
```

## Code Style Guidelines

### Python Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use meaningful variable names (e.g., `monthly_revenue` not `mr`)
- Maximum line length: 100 characters
- Use docstrings for all functions

**Example:**
```python
def calculate_projections(current_revenue, growth_rate, months=48):
    """
    Calculate monthly revenue projections based on growth assumptions.

    Args:
        current_revenue (float): Current monthly revenue in lakhs
        growth_rate (float): Monthly growth rate as percentage
        months (int): Number of months to project (default: 48)

    Returns:
        pd.DataFrame: Projections with columns for revenue and payments
    """
    # Implementation
```

### Streamlit Best Practices
- Use st.cache_data for expensive computations
- Keep UI updates in main thread
- Use columns for layout consistency
- Add help text with (?) icons for clarity

### Comments
- Write self-documenting code first
- Add comments for complex business logic
- Explain "why" not "what" in comments

## Making Changes

### Branching Strategy
We use a simplified Git Flow:

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

### Creating a Feature Branch

```bash
# Update your local repository
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Making Commits

1. Make focused, atomic commits
2. Test your changes before committing
3. Follow commit message conventions (see below)

## Commit Message Conventions

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(projections): add quarterly summary view

Add quarterly aggregation to cash flow tab for easier
board meeting reporting.

Closes #23
```

```
fix(calculations): correct LTV calculation formula

LTV was using 12-month lifetime instead of 6-month.
Updated to match investment memo assumptions.

Fixes #45
```

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] All functions have docstrings
- [ ] README updated (if needed)
- [ ] No console.log or debug code left
- [ ] Tested locally with sample data

### Submitting PR

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request on GitHub**
   - Use the PR template
   - Link related issues
   - Add screenshots for UI changes
   - Request review from maintainers

3. **Address Review Comments**
   - Make requested changes
   - Reply to comments
   - Push updates to same branch

4. **Merge**
   - Maintainer will merge when approved
   - Delete your branch after merge

## Testing Guidelines

### Manual Testing Checklist

Since we don't have automated tests yet, please verify:

- [ ] App starts without errors
- [ ] All sidebar inputs work correctly
- [ ] Charts render properly
- [ ] Calculations are accurate (compare with Excel)
- [ ] Downloads work (CSV, JSON)
- [ ] Responsive on different screen sizes
- [ ] No console errors in browser

### Test Different Scenarios

- High growth rate (>10%)
- Low growth rate (<3%)
- Edge cases (zero values, very large numbers)
- Different months (1, 12, 36, 48+)

## Getting Help

### Questions or Issues?

- **Quick Questions:** Open a [Discussion](../../discussions)
- **Bug Reports:** Open an [Issue](../../issues) with bug template
- **Feature Requests:** Open an [Issue](../../issues) with feature template
- **Email:** tech-support@vinmoventures.com

### Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [Project README](README.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment. Be:
- Respectful and professional
- Collaborative and helpful
- Open to feedback
- Patient with newcomers

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Unprofessional conduct

## Recognition

Contributors will be:
- Listed in CHANGELOG.md
- Mentioned in release notes
- Added to README acknowledgments (for significant contributions)

---

**Thank you for contributing to AdNexus Investment Tracker!**

Your contributions help make this tool better for the entire team.
