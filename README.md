# job-auto-apply
# Job Application Automation API

This is a Flask + Playwright-based automation service that:
- Logs in with Google (if required)
- Fills out application forms
- Solves CAPTCHAs (placeholder)
- Supports multiple jobs in a single POST request

### Run Locally

```bash
docker build -t job-bot .
docker run -p 8080:8080 job-bot
