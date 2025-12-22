# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

**IMPORTANT:** Do NOT create public GitHub issues for security vulnerabilities.

### How to Report

1. **Email:** Send details to security@vinmoventures.com
2. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Timeline:** Depends on severity (critical: 24-48h, high: 1 week, medium: 2 weeks)

## Security Best Practices

### For Developers

- Never commit `.streamlit/secrets.toml` to git
- Never hardcode credentials in code
- Use environment variables for sensitive data
- Keep dependencies up to date
- Review code for security issues before committing

### For Users

- Do not share the application URL publicly
- Use HTTPS in production
- Implement authentication before deployment
- Regularly update Python packages
- Monitor access logs

## Known Security Considerations

1. **No Built-in Authentication:** The current version does not include authentication.
   Add authentication before deploying to production.

2. **Data Privacy:** This application processes financial data. Ensure proper access
   controls and data encryption in production environments.

3. **Dependencies:** Regularly update dependencies to patch known vulnerabilities:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## Security Updates

Security updates will be released as patch versions (e.g., 1.0.1) and documented
in the CHANGELOG.md with a `[Security]` tag.

---

**Last Updated:** December 22, 2025
